#!/bin/bash

echo "vfio-pci" > /sys/bus/pci/devices/0000:01:00.0/iommu_group/devices/0000:01:00.0/driver_override
echo "vfio-pci" > /sys/bus/pci/devices/0000:01:00.0/iommu_group/devices/0000:01:00.1/driver_override
modprobe -r nvidia_drm nvidia_modeset nvidia_uvm nvidia
modprobe -i vfio-pci
