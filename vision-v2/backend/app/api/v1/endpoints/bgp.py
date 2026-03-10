"""
BGP Prefix-list API endpoints
"""
import os
import sys
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.bgp import (
    BGPPrefixListRequest,
    BGPPrefixListResponse,
    DeviceInfo,
    DeviceListResponse
)

# Add scripts directory to path for importing the bgp updater
scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from bgp_prefixlist_updater import update_bgp_prefix_list

router = APIRouter()

# In-memory device storage (replace with database in production)
# This is a sample list of devices - in production, this should come from a database
SAMPLE_DEVICES = [
    DeviceInfo(
        id="1",
        name="Juniper MX-01",
        hostname="192.168.1.1",
        port=830,
        username="admin",
        password="admin123"
    ),
    DeviceInfo(
        id="2",
        name="Juniper MX-02",
        hostname="192.168.1.2",
        port=830,
        username="admin",
        password="admin123"
    ),
    DeviceInfo(
        id="3",
        name="Juniper MX-Edge-01",
        hostname="10.0.1.1",
        port=830,
        username="admin",
        password="admin123"
    ),
]


@router.get("/devices", response_model=DeviceListResponse)
async def get_devices(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get list of available Juniper MX devices for BGP prefix-list updates.
    """
    return DeviceListResponse(devices=SAMPLE_DEVICES)


@router.post("/update-prefix-list", response_model=BGPPrefixListResponse)
async def update_prefix_list(
    request: BGPPrefixListRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update BGP prefix-list on a Juniper MX device.
    
    This endpoint:
    1. Uses bgpq4 to generate prefix-list from the specified ASN
    2. Connects to the device via NETCONF
    3. Applies the prefix-list configuration
    
    Required:
    - device_id: ID of the target device
    - asn: Autonomous System number (e.g., "AS15169" or "15169")
    - prefix_list_name: Name for the prefix-list
    """
    # Find the device
    device = None
    for d in SAMPLE_DEVICES:
        if d.id == request.device_id:
            device = d
            break
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID '{request.device_id}' not found"
        )
    
    try:
        # Call the BGP prefix-list updater
        result = update_bgp_prefix_list(
            device_hostname=device.hostname,
            device_username=device.username,
            device_password=device.password,
            asn=request.asn,
            prefix_list_name=request.prefix_list_name,
            device_port=device.port,
            protocol=request.protocol,
            max_prefixes=request.max_prefixes
        )
        
        return BGPPrefixListResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update prefix-list: {str(e)}"
        )


@router.get("/devices/{device_id}", response_model=DeviceInfo)
async def get_device(
    device_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get device details by ID.
    """
    for device in SAMPLE_DEVICES:
        if device.id == device_id:
            return device
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Device with ID '{device_id}' not found"
    )
