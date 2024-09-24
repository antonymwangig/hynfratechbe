import libvirt,uuid,subprocess
from rest_framework import viewsets,permissions,views,response,status
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer
from django_filters.rest_framework import DjangoFilterBackend

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state', 'project']


class CreateVMAPIView(views.APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request,data):
        
        vm_name = f"example-vm-{uuid.uuid4()}"
        disk_image_path = f"/var/lib/libvirt/images/{vm_name}.qcow2"
        xml_config =f"""
        <domain type='qemu'>
            <name>example-vm</name>
            <memory unit='KiB'>1048576</memory>
            <vcpu placement='static'>1</vcpu>
            <os>
                <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
                <boot dev='hd'/>
            </os>
            <devices>
                <disk type='file' device='disk'>
                    <driver name='qemu' type='qcow2'/>
                    <source file='{disk_image_path}'/>
                    <target dev='vda' bus='virtio'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                </disk>
                <interface type='network'>
                    <source network='default'/>
                    <model type='virtio'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                </interface>
            </devices>
        </domain>
        """
        
        
        try:
            subprocess.run(
                ["qemu-img", "create", "-f", "qcow2", disk_image_path, "10G"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            return response.Response({'error': f'Failed to create disk image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        conn = libvirt.open('qemu:///system')
        if conn is None:
            return response.Response({'error': 'Failed to open connection to qemu:///system'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vm = conn.createXML(xml_config, 0)
            VirtualMachine.objects.create
            return response.Response({'status': 'VM created', 'name': vm.name()}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            conn.close()
            
class StartVMAPIView(views.APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, vm_name):
        conn = libvirt.open('qemu:///system')
        if conn is None:
            return response.Response({'error': 'Failed to open connection to qemu:///system'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vm = conn.lookupByName(vm_name)
            if vm.isActive():
                return response.Response({'status': 'VM is already running', 'name': vm_name}, status=status.HTTP_200_OK)

            vm.create()
            return response.Response({'status': 'VM started', 'name': vm_name}, status=status.HTTP_200_OK)
        except libvirt.libvirtError as e:
            return response.Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        finally:
            conn.close()