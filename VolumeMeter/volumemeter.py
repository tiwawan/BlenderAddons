bl_info = {
    "name": "Volume Meter",
    "category": "Object",
}

from bpy import *
import random


class VolumeMeter(types.Operator):
    """
    Volume Meter
    Array active object so that it appears like a sound volume meter.
    """
    bl_idname = "object.volume_meter"
    bl_label = "Volume Meter"
    bl_options = {'REGISTER', 'UNDO'}

    loop = props.IntProperty(name="Bars", default=10, min=1, max=500)
    max_height = props.IntProperty(name="Maximum Height", default=10, min=1, max=100)
    offset_coeff = props.FloatProperty(name="Offset X", default=1.3, min=1.0, max=10.0)
    offset_coeff_z = props.FloatProperty(name="Offset Z", default=1.3, min=1.0, max=10.0)
    seed = props.IntProperty(name="Seed", default=0, min=0, max=65535)
    ave_times = props.IntProperty(name="Random Value Average Times", default=2, min=1, max=50)
    

    def execute(self, context):
        random.seed(self.seed)
        scene = context.scene
        obj = scene.objects.active
        offset_base = obj.dimensions[0]
        ops.object.modifier_add(type='ARRAY')
        
        loop = 30
        for i in range(0, self.loop):
            obj = scene.objects.active
            
            count = 0
            for j in range(0,self.ave_times):
                count = count+random.randint(1,self.max_height)
            count = int(count/self.ave_times)
            obj.modifiers[-1].count = count 
            
            obj.modifiers[-1].relative_offset_displace[0]=0
            obj.modifiers[-1].relative_offset_displace[1]=0
            obj.modifiers[-1].relative_offset_displace[2]=self.offset_coeff_z
            ops.object.duplicate_move()
            ops.transform.translate(value=(self.offset_coeff*offset_base,0,0))
        return {'FINISHED'}

def register():
    utils.register_class(VolumeMeter)


def unregister():
    utils.unregister_class(VolumeMeter)


if __name__ == "__main__":
    register()

