"""
BGP Prefix-list schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """Device information schema"""
    id: str
    name: str
    hostname: str
    port: int = 830
    username: str
    password: str


class BGPPrefixListRequest(BaseModel):
    """Request schema for BGP prefix-list update"""
    device_id: str = Field(..., description="Device ID to update")
    asn: str = Field(..., description="Autonomous System number (e.g., AS15169)")
    prefix_list_name: str = Field(..., description="Name of the prefix-list")
    protocol: str = Field(default="ipv4", description="Protocol: ipv4 or ipv6")
    max_prefixes: Optional[int] = Field(None, description="Maximum number of prefixes")


class BGPPrefixListResponse(BaseModel):
    """Response schema for BGP prefix-list update"""
    success: bool
    device: str
    prefix_list: str
    asn: str
    prefixes_generated: int
    prefixes_applied: int
    message: str
    details: Optional[dict] = None


class DeviceListResponse(BaseModel):
    """Response schema for device list"""
    devices: List[DeviceInfo]
