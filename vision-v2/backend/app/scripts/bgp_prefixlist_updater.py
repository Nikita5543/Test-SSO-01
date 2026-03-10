#!/usr/bin/env python3
"""
BGP Prefix-list Updater for Juniper MX devices

This script updates BGP prefix-lists on Juniper MX devices using bgpq4 utility
and NETCONF protocol for device configuration.

Requirements:
    - bgpq4: https://github.com/bgp/bgpq4 (must be installed and in PATH)
    - ncclient: pip install ncclient
    - lxml: pip install lxml

Usage:
    python bgp_prefixlist_updater.py --device <hostname> --asn <ASN> --prefix-list <name> [options]

Example:
    python bgp_prefixlist_updater.py --device 192.168.1.1 --asn AS15169 --prefix-list GOOGLE-PREFIXES
"""

import argparse
import subprocess
import sys
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from ncclient import manager
from ncclient.operations import RPCError
from lxml import etree


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class DeviceConfig:
    """Device connection configuration"""
    hostname: str
    username: str
    password: str
    port: int = 830
    timeout: int = 30


@dataclass
class PrefixListConfig:
    """Prefix-list configuration"""
    name: str
    asn: str
    protocol: str = "ipv4"  # ipv4 or ipv6
    max_prefixes: Optional[int] = None


class Bgpq4Runner:
    """Runs bgpq4 utility to generate prefix-lists"""
    
    SUPPORTED_PROTOCOLS = {"ipv4", "ipv6"}
    
    def __init__(self, bgpq4_path: str = "bgpq4"):
        self.bgpq4_path = bgpq4_path
    
    def _check_bgpq4(self) -> bool:
        """Check if bgpq4 is available"""
        try:
            result = subprocess.run(
                [self.bgpq4_path, "-v"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def generate_prefix_list(
        self,
        asn: str,
        prefix_list_name: str,
        protocol: str = "ipv4",
        max_prefixes: Optional[int] = None
    ) -> Tuple[bool, List[str], str]:
        """
        Generate prefix-list using bgpq4
        
        Args:
            asn: Autonomous System number (e.g., "AS15169" or "15169")
            prefix_list_name: Name for the prefix-list
            protocol: "ipv4" or "ipv6"
            max_prefixes: Maximum number of prefixes to generate
            
        Returns:
            Tuple of (success, prefixes, error_message)
        """
        if not self._check_bgpq4():
            return False, [], "bgpq4 is not installed or not in PATH"
        
        if protocol not in self.SUPPORTED_PROTOCOLS:
            return False, [], f"Unsupported protocol: {protocol}"
        
        # Build bgpq4 command
        cmd = [
            self.bgpq4_path,
            "-Jl",  # Juniper format, single line output
            prefix_list_name
        ]
        
        # Add protocol flag
        if protocol == "ipv6":
            cmd.append("-6")
        else:
            cmd.append("-4")
        
        # Add max prefixes limit if specified
        if max_prefixes:
            cmd.extend(["-m", str(max_prefixes)])
        
        # Add ASN
        # Remove 'AS' prefix if present
        asn_clean = asn.upper().replace("AS", "") if asn.upper().startswith("AS") else asn
        cmd.append(f"AS{asn_clean}")
        
        logger.info(f"Running bgpq4 command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown error from bgpq4"
                logger.error(f"bgpq4 failed: {error_msg}")
                return False, [], error_msg
            
            # Parse output - bgpq4 returns Juniper config format
            output = result.stdout.strip()
            logger.debug(f"bgpq4 output: {output}")
            
            # Extract prefixes from Juniper format output
            prefixes = self._parse_juniper_prefix_list(output)
            
            return True, prefixes, ""
            
        except subprocess.TimeoutExpired:
            return False, [], "bgpq4 command timed out"
        except Exception as e:
            return False, [], f"Error running bgpq4: {str(e)}"
    
    def _parse_juniper_prefix_list(self, output: str) -> List[str]:
        """
        Parse Juniper format output and extract prefixes
        
        Example output format:
        policy-options {
            prefix-list GOOGLE-PREFIXES {
                8.8.4.0/24;
                8.8.8.0/24;
                ...
            }
        }
        """
        prefixes = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for lines ending with semicolon that contain prefixes
            if line.endswith(';') and ('/' in line):
                # Remove semicolon and whitespace
                prefix = line.rstrip(';').strip()
                if prefix:
                    prefixes.append(prefix)
        
        return prefixes


class JuniperNetconfClient:
    """NETCONF client for Juniper devices"""
    
    # Juniper namespace
    JUNOS_NS = "http://yang.juniper.net/junos/conf/root"
    JUNOS_CONF_NS = "http://xml.juniper.net/xnm/1.1/xnm"
    
    def __init__(self, device_config: DeviceConfig):
        self.config = device_config
        self.connection = None
    
    def connect(self) -> bool:
        """Establish NETCONF connection to device"""
        try:
            logger.info(f"Connecting to {self.config.hostname}:{self.config.port}")
            self.connection = manager.connect(
                host=self.config.hostname,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                timeout=self.config.timeout,
                device_params={'name': 'junos'},
                hostkey_verify=False,
                allow_agent=False,
                look_for_keys=False
            )
            logger.info(f"Successfully connected to {self.config.hostname}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.config.hostname}: {str(e)}")
            return False
    
    def disconnect(self):
        """Close NETCONF connection"""
        if self.connection:
            try:
                self.connection.close_session()
                logger.info(f"Disconnected from {self.config.hostname}")
            except Exception as e:
                logger.warning(f"Error during disconnect: {str(e)}")
            finally:
                self.connection = None
    
    def __enter__(self):
        if not self.connect():
            raise ConnectionError(f"Could not connect to {self.config.hostname}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def update_prefix_list(
        self,
        prefix_list_name: str,
        prefixes: List[str],
        protocol: str = "ipv4"
    ) -> Tuple[bool, str]:
        """
        Update prefix-list on Juniper device
        
        Args:
            prefix_list_name: Name of the prefix-list
            prefixes: List of prefixes to set
            protocol: "ipv4" or "ipv6"
            
        Returns:
            Tuple of (success, message)
        """
        if not self.connection:
            return False, "Not connected to device"
        
        try:
            # Build configuration XML
            config_xml = self._build_prefix_list_config(prefix_list_name, prefixes)
            logger.debug(f"Configuration XML: {config_xml}")
            
            # Lock configuration
            logger.info("Locking configuration")
            self.connection.lock(target='candidate')
            
            try:
                # Load configuration
                logger.info("Loading configuration")
                self.connection.edit_config(
                    target='candidate',
                    config=config_xml
                )
                
                # Validate configuration
                logger.info("Validating configuration")
                self.connection.validate(source='candidate')
                
                # Commit configuration
                logger.info("Committing configuration")
                commit_result = self.connection.commit()
                
                logger.info(f"Successfully updated prefix-list '{prefix_list_name}'")
                return True, f"Prefix-list '{prefix_list_name}' updated with {len(prefixes)} prefixes"
                
            except RPCError as e:
                # Discard changes on error
                logger.warning("Discarding configuration changes due to error")
                self.connection.discard_changes()
                raise e
            finally:
                # Unlock configuration
                logger.info("Unlocking configuration")
                self.connection.unlock(target='candidate')
                
        except RPCError as e:
            error_msg = f"NETCONF RPC error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error updating prefix-list: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _build_prefix_list_config(self, name: str, prefixes: List[str]) -> str:
        """
        Build Juniper configuration XML for prefix-list
        
        Args:
            name: Prefix-list name
            prefixes: List of prefixes
            
        Returns:
            Configuration XML string
        """
        # Build prefix-list entries
        prefix_entries = ""
        for prefix in prefixes:
            prefix_entries += f"""
                        <name>{prefix}</name>"""
        
        # Build complete configuration XML
        config = f"""<configuration>
            <policy-options>
                <prefix-list>
                    <name>{name}</name>
                    {prefix_entries}
                </prefix-list>
            </policy-options>
        </configuration>"""
        
        return config
    
    def get_prefix_list(self, prefix_list_name: str) -> Tuple[bool, Optional[List[str]], str]:
        """
        Get current prefix-list from device
        
        Args:
            prefix_list_name: Name of the prefix-list
            
        Returns:
            Tuple of (success, prefixes, message)
        """
        if not self.connection:
            return False, None, "Not connected to device"
        
        try:
            # Build filter for specific prefix-list
            filter_xml = f"""
            <policy-options>
                <prefix-list>
                    <name>{prefix_list_name}</name>
                </prefix-list>
            </policy-options>
            """
            
            # Get configuration
            result = self.connection.get_config(
                source='running',
                filter=('subtree', filter_xml)
            )
            
            # Parse result
            data = result.data_xml
            logger.debug(f"Get config result: {data}")
            
            # Parse prefixes from XML
            root = etree.fromstring(data.encode())
            namespaces = {
                'junos': self.JUNOS_NS,
                'conf': 'http://yang.juniper.net/junos/conf/policy-options'
            }
            
            prefixes = []
            # Try different XPath expressions
            for elem in root.iter():
                if elem.tag.endswith('name') and '/' in str(elem.text):
                    prefixes.append(str(elem.text))
            
            return True, prefixes, f"Found {len(prefixes)} prefixes"
            
        except Exception as e:
            error_msg = f"Error getting prefix-list: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg


class BgpPrefixListUpdater:
    """Main class for updating BGP prefix-lists"""
    
    def __init__(
        self,
        device_config: DeviceConfig,
        bgpq4_path: str = "bgpq4"
    ):
        self.device_config = device_config
        self.bgpq4 = Bgpq4Runner(bgpq4_path)
    
    def update(
        self,
        prefix_list_config: PrefixListConfig
    ) -> Dict:
        """
        Update prefix-list on device
        
        Args:
            prefix_list_config: Prefix-list configuration
            
        Returns:
            Dictionary with operation result
        """
        result = {
            "success": False,
            "device": self.device_config.hostname,
            "prefix_list": prefix_list_config.name,
            "asn": prefix_list_config.asn,
            "prefixes_generated": 0,
            "prefixes_applied": 0,
            "message": "",
            "details": {}
        }
        
        # Step 1: Generate prefix-list using bgpq4
        logger.info(f"Generating prefix-list for ASN {prefix_list_config.asn}")
        success, prefixes, error = self.bgpq4.generate_prefix_list(
            asn=prefix_list_config.asn,
            prefix_list_name=prefix_list_config.name,
            protocol=prefix_list_config.protocol,
            max_prefixes=prefix_list_config.max_prefixes
        )
        
        if not success:
            result["message"] = f"Failed to generate prefix-list: {error}"
            return result
        
        result["prefixes_generated"] = len(prefixes)
        result["details"]["generated_prefixes"] = prefixes
        logger.info(f"Generated {len(prefixes)} prefixes")
        
        if not prefixes:
            result["message"] = "No prefixes generated - ASN may have no announced prefixes"
            return result
        
        # Step 2: Connect to device and apply configuration
        try:
            with JuniperNetconfClient(self.device_config) as client:
                # Get current prefix-list for comparison
                success, current_prefixes, _ = client.get_prefix_list(prefix_list_config.name)
                if success and current_prefixes:
                    result["details"]["previous_prefixes"] = current_prefixes
                
                # Apply new prefix-list
                success, message = client.update_prefix_list(
                    prefix_list_name=prefix_list_config.name,
                    prefixes=prefixes,
                    protocol=prefix_list_config.protocol
                )
                
                if success:
                    result["success"] = True
                    result["prefixes_applied"] = len(prefixes)
                    result["message"] = message
                else:
                    result["message"] = f"Failed to apply prefix-list: {message}"
                    
        except ConnectionError as e:
            result["message"] = f"Connection failed: {str(e)}"
        except Exception as e:
            result["message"] = f"Unexpected error: {str(e)}"
        
        return result


def main():
    """Main entry point for CLI usage"""
    parser = argparse.ArgumentParser(
        description="Update BGP prefix-list on Juniper MX devices"
    )
    
    # Device connection arguments
    parser.add_argument(
        "--device", "-d",
        required=True,
        help="Device hostname or IP address"
    )
    parser.add_argument(
        "--username", "-u",
        required=True,
        help="Device username"
    )
    parser.add_argument(
        "--password", "-p",
        required=True,
        help="Device password"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=830,
        help="NETCONF port (default: 830)"
    )
    
    # Prefix-list arguments
    parser.add_argument(
        "--asn", "-a",
        required=True,
        help="Autonomous System number (e.g., AS15169 or 15169)"
    )
    parser.add_argument(
        "--prefix-list", "-n",
        required=True,
        help="Prefix-list name"
    )
    parser.add_argument(
        "--protocol",
        choices=["ipv4", "ipv6"],
        default="ipv4",
        help="IP protocol version (default: ipv4)"
    )
    parser.add_argument(
        "--max-prefixes", "-m",
        type=int,
        help="Maximum number of prefixes to generate"
    )
    
    # Other options
    parser.add_argument(
        "--bgpq4-path",
        default="bgpq4",
        help="Path to bgpq4 executable (default: bgpq4)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create device configuration
    device_config = DeviceConfig(
        hostname=args.device,
        username=args.username,
        password=args.password,
        port=args.port
    )
    
    # Create prefix-list configuration
    prefix_list_config = PrefixListConfig(
        name=args.prefix_list,
        asn=args.asn,
        protocol=args.protocol,
        max_prefixes=args.max_prefixes
    )
    
    # Create updater and run
    updater = BgpPrefixListUpdater(
        device_config=device_config,
        bgpq4_path=args.bgpq4_path
    )
    
    result = updater.update(prefix_list_config)
    
    # Print result
    import json
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


# Function for programmatic use (called from FastAPI)
def update_bgp_prefix_list(
    device_hostname: str,
    device_username: str,
    device_password: str,
    asn: str,
    prefix_list_name: str,
    device_port: int = 830,
    protocol: str = "ipv4",
    max_prefixes: Optional[int] = None,
    bgpq4_path: str = "bgpq4"
) -> Dict:
    """
    Update BGP prefix-list programmatically
    
    This function can be called from FastAPI or other Python code
    
    Args:
        device_hostname: Device hostname or IP
        device_username: Device username
        device_password: Device password
        asn: Autonomous System number
        prefix_list_name: Name of the prefix-list
        device_port: NETCONF port (default: 830)
        protocol: "ipv4" or "ipv6"
        max_prefixes: Maximum number of prefixes
        bgpq4_path: Path to bgpq4 executable
        
    Returns:
        Dictionary with operation result
    """
    device_config = DeviceConfig(
        hostname=device_hostname,
        username=device_username,
        password=device_password,
        port=device_port
    )
    
    prefix_list_config = PrefixListConfig(
        name=prefix_list_name,
        asn=asn,
        protocol=protocol,
        max_prefixes=max_prefixes
    )
    
    updater = BgpPrefixListUpdater(
        device_config=device_config,
        bgpq4_path=bgpq4_path
    )
    
    return updater.update(prefix_list_config)


if __name__ == "__main__":
    main()
