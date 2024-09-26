import libvirt,uuid,subprocess
from rest_framework import viewsets,permissions,views,response,status
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal

from payments.models import Payment

from plans.models import ServicePlan

from users.logger import log_user_action

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state']
    

class CreateVMAPIView(views.APIView):
    def post(self, request):
        data=request.data
        print(data)
        plan=ServicePlan.objects.get(id=data["plan"])
        vm_name = f"vm-{uuid.uuid4()}"
        disk_image_path = f"/var/lib/libvirt/images/{vm_name}.qcow2"
        xml_config =f"""
        <domain type='qemu'>
            <name>{vm_name}</name>
            <memory unit='KiB'>{plan.memory_size}</memory>
            <vcpu placement='static'>{plan.vcpu_count}</vcpu>
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
                    <!-- First Network Interface (NAT) -->
                <interface type='network'>
                    <source network='default'/>
                    <model type='virtio'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                </interface>
                
                <!-- Second Network Interface (Bridge) -->
                <interface type='bridge'>
                    <source bridge='br0'/>
                    <model type='virtio'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                </interface>

                <!-- QEMU Guest Agent Channel -->
                <channel type='unix'>
                    <source mode='bind'/>
                    <target type='virtio' name='org.qemu.guest_agent.0'/>
                    <alias name='channel0'/>
                </channel>

            </devices>
        </domain>
        """
        
        
        try:
            subprocess.run(
                ["qemu-img", "create", "-f", "qcow2", disk_image_path, "10G"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            log_user_action(request.user,"CREATE VM",f'Failed to create disk image: {str(e)}')
            return response.Response({'error': f'Failed to create disk image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        conn = libvirt.open('qemu:///system')
        if conn is None:
            log_user_action(request.user,"CREATE VM","Failed to open connection to qemu:///system")
            return response.Response({'error': 'Failed to open connection to qemu:///system'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if True:
            amount=round(Decimal((Decimal(plan.price)*Decimal(0.9))+(Decimal(plan.price)*Decimal(0.9)*Decimal(0.2))),2)
            order_no=str(vm_name).replace("vm-","OR-")
            payment_info=data["card"]      
            payment_info["amount"]=amount      
            try:
                payment_info.pop("cvv")
                
                payment_info["status"]="COMPLETED"

            except:
                try:
                    paymentObj=Payment.objects.get(id=payment_info.pop("id"))
                except:
                    paymentObj = Payment.objects.all().order_by("-payment_date").first()
                payment_info.pop("card_number")
                payment_info["card_number"]=paymentObj.card_number
                payment_info["full_name"]=paymentObj.full_name
                payment_info["expiration"]=paymentObj.expiration
                
            vm = conn.createXML(xml_config, 0)
            
            vm_status = vm.state()[0]
            status_map = {
                libvirt.VIR_DOMAIN_NOSTATE: 'No state',
                libvirt.VIR_DOMAIN_RUNNING: 'Running',
                libvirt.VIR_DOMAIN_BLOCKED: 'Blocked',
                libvirt.VIR_DOMAIN_PAUSED: 'Paused',
                libvirt.VIR_DOMAIN_SHUTDOWN: 'Shutdown',
                libvirt.VIR_DOMAIN_SHUTOFF: 'Shutoff',
                libvirt.VIR_DOMAIN_CRASHED: 'Crashed',
            }
            vm_current_status = status_map.get(vm_status, 'Unknown')

            Payment.objects.update_or_create(order_no=order_no,user=request.user,defaults=payment_info)
            log_user_action(request.user,"CREATE VM",f"Payment  Order no {vm_name}  Amount {amount}")
            VirtualMachine.objects.create(
                vm_name=vm.name(),
                name=data["name"],
                vcpu_count=plan.vcpu_count,
                disk_size=plan.disk_size,
                disk_image_path=disk_image_path,
                memory_size=plan.memory_size,
                owner=request.user,
                state=vm_current_status
            )
            
            log_user_action(request.user,"CREATE VM",f"Created VM {data['name']}  VM_NAME {vm.name()}")
            return response.Response({'status': True,"message":"VM CREATED", 'name': vm.name()}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     log_user_action(request.user,"CREATE VM",f"Error  {str(e)}")
        #     return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # finally:
        #     conn.close()
            
class StartVMAPIView(views.APIView):
    def post(self, request):
        data=request.data
        virtualMachine=VirtualMachine.objects.get(owner=request.user,id=data["id"])
        conn = libvirt.open('qemu:///system')
        if conn is None:
            log_user_action(request.user,"START VM",'Failed to open connection to qemu:///system')

            return response.Response({'error': 'Failed to open connection to qemu:///system'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vm = conn.lookupByName(virtualMachine.vm_name)
            if vm.isActive():
                log_user_action(request.user,"START VM",f'VM {virtualMachine.name}  VM_NAME {virtualMachine.vm_name} is already running')
                return response.Response({'status': 'VM is already running', 'name': vm_name}, status=status.HTTP_200_OK)

            vm.create()
            log_user_action(request.user,"START VM",f'VM  STARTED {virtualMachine.name}  VM_NAME {virtualMachine.vm_name}' )
                
            return response.Response({'status': 'VM started', 'name': vm_name}, status=status.HTTP_200_OK)
        except libvirt.libvirtError as e:
            log_user_action(request.user,"START VM",f'ERROR {str(e)}' )
            
            return response.Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        finally:
            conn.close()
            
            
            
class VMStateView(views.APIView):
    def post(self, request):
        data=request.data
        virtualMachine=VirtualMachine.objects.get(owner=request.user,id=data["id"])
        conn = libvirt.open('qemu:///system')
        if conn is None:
            return response.Response({'error': 'Failed to open connection to qemu:///system'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Step 2: Find the VM by name
            try:
                vm = conn.lookupByName(virtualMachine.vm_name)
            except libvirt.libvirtError:
                return response.Response({'error': f'VM with name {vm_name} not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Step 3: Check the VM status
            vm_status = vm.state()[0]
            status_map = {
                libvirt.VIR_DOMAIN_NOSTATE: 'No state',
                libvirt.VIR_DOMAIN_RUNNING: 'Running',
                libvirt.VIR_DOMAIN_BLOCKED: 'Blocked',
                libvirt.VIR_DOMAIN_PAUSED: 'Paused',
                libvirt.VIR_DOMAIN_SHUTDOWN: 'Shutdown',
                libvirt.VIR_DOMAIN_SHUTOFF: 'Shutoff',
                libvirt.VIR_DOMAIN_CRASHED: 'Crashed',
            }
            vm_current_status = status_map.get(vm_status, 'Unknown')
            print("interfaces")
            if vm.isActive() == 1:
                
                interfaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
                print(interfaces)
                for interface_name, val in interfaces.items():
                    if val['addrs']:
                        for addr in val['addrs']:
                            if addr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                                print(addr['addr']) 
            else:
                #"VM is not running"
                pass
            virtualMachine.status = vm_current_status
            virtualMachine.save()
            
            return response.Response({
                'status': 'VM status retrieved',
                'id': virtualMachine.id,
                'vm_status': vm_current_status
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        finally:
            conn.close()
    
    