import bpy
import binascii
import struct
from liblas import file
from liblas import header
import multiprocessing
import time

# Blender Addon Information
# Used by User Preferences > Addons
bl_info = {
    "name" : "LiDAR Importer",
    "author" : "Brian Cordell Hynds",
    "version" : (0, 1),
    "blender" : (2, 6, 0),
    "description" : "LiDAR File Importer with 3D Object Recognition",
    "category" : "Import-Export",
    "location" : "File > Import"
}

# Not In Use Yet: For Multiprocessing Module
def worker(ImportLiDARData):
    print("")

# Not In Use Yet: For Multiprocessing Module
def worker_complete(result):
    print("")

def read_lidar_data(context, filepath, use_some_setting):
    print("running read_lidar_data")

    # importer start time
    start_time = time.time()

    # empty list for coordinates
    coords = []

    # open the file
    f = file.File(filepath,mode='r')

    # lets get some header information from the file
    fileCount = f.header.count

    for p in f:
        coords.append((p.x, p.y, p.z))
        print("XYZ: ", p.x, ", ", p.y, ", ", p.z)

    me = bpy.data.meshes.new("LidarMesh")
    obj = bpy.data.objects.new("LidarObject", me)
    bpy.context.scene.objects.link(obj)
    me.from_pydata(coords,[],[])

    bpy.context.scene.objects.active = obj
    bpy.data.objects['LidarObject'].select = True
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    obj.location = (0,0,0)

    print(str(fileCount) + " verticies in the LiDAR Point Cloud")

    print("Total time to process (seconds): ", time.time() - start_time)
    print("File: ", filepath)

    print("completed read_lidar_data...")
    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportLiDARData(Operator, ImportHelper):
    """Load a LiDAR .las file"""
    bl_idname = "import_mesh.lidar"  # important since its how bpy.ops.import_mesh.lidar is constructed
    bl_label = "Import LiDAR File"

    # ImportHelper mixin class uses this
    filename_ext = ".las"

    filter_glob = StringProperty(
            default="*.las",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
            name="Example Boolean",
            description="Example Tooltip",
            default=True,
            )

    def execute(self, context):
        return read_lidar_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportLiDARData.bl_idname, text="LiDAR Format (.las)")


def register():
    bpy.utils.register_class(ImportLiDARData)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportLiDARData)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_mesh.lidar('INVOKE_DEFAULT')
