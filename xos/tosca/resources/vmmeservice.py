from services.vmme.models import VMMEService
from service import XOSService

class XOSVMMEService(XOSService):
	provides = "tosca.nodes.VMMEService"
	xos_model = VMMEService
	copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber"]