import bpy
from bpy import context
import sys
import time
import subprocess
from pathlib import Path

py_path = Path(sys.prefix) / "bin"
py_exec = next(py_path.glob("python*"))
subprocess.call([str(py_exec), "-m", "ensurepip"])
subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "laspy"])

import laspy
from laspy.file import File
import numpy as np

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator

bl_info = {
  "name" : "LiDAR Importer",
  "author" : "Brian C. Hynds",
  "version" : (0, 1),
  "blender" : (2, 80, 0),
  "description" : "LiDAR File Importer with 3D Object Recognition",
  "category" : "Import-Export",
  "location" : "File > Import"
}

class ImportLiDARData(Operator, ImportHelper):
    """Load a LiDAR .las file"""
    bl_idname = "import_mesh.lidar"  # important since its how bpy.ops.import_mesh.lidar is constructed
    bl_label = "Import LiDAR File"

    # ImportHelper mixin class uses this
    filename_ext = ".las"

    filter_glob = StringProperty(
        default="*.las",
        options={'HIDDEN'}
    )

    # List of operator properties, the attributes will be assigned to the class instance from the operator settings before calling.
    pointCloudResolution = IntProperty(
        name="Point Resolution",
        min=1,
        max=100,
        description="This is a percentage resolution of the total point cloud to import.",
        default=100
    )

    cleanScene = BoolProperty(
        name="Empty Scene",
        description="Enable to remove all objects from current scene",
        default=True
    )

    def execute(self, context):
        return read_lidar_data(context, self.filepath, self.pointCloudResolution, self.cleanScene)

class LiDARPanel(bpy.types.Panel):
    """LiDAR Addon Panel"""
    bl_label = "LiDAR Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("import_mesh.lidar")

def read_lidar_data(context, filepath, pointCloudResolution, cleanScene):

    print("running read_lidar_data")

    # importer start time
    start_time = time.time()

    # empty list for coordinates
    coords = []

    # reference to scene
    scn = bpy.context.scene

    # clear the scene if specified during file selection:
    if (cleanScene):
        for obj in scn.objects:
            obj.select_set(state=True)
        bpy.ops.object.delete()

    # create a new mesh
    me = bpy.data.meshes.new("LidarMesh")

    # create a new object with the mesh
    obj = bpy.data.objects.new("LidarObject", me)

    # link the mesh to the scene
    scn.collection.objects.link(obj)

    inFile = File(filepath, mode='r')
    # Grab all of the points from the file.
    point_records = inFile.points
    print(f"POINTS: {len(point_records)}")

    coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()
    me.from_pydata(coords,[],[])
    me.update()
    print(f"LiDAR Mesh Verts: {len(me.vertices)}")

    inFile.close()

    return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportLiDARData.bl_idname, text="LiDAR Format (.las)")

def register():
    print("REGISTERING LIDAR-IMPORTER...")
    bpy.utils.register_class(ImportLiDARData)
    bpy.utils.register_class(LiDARPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    print("SUCCESS!")

def unregister():
    print("UNREGISTERING LIDAR-IMPORTER...")
    bpy.utils.unregister_class(ImportLiDARData)
    bpy.utils.unregister_class(LiDARPanel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    print("GOODBYE, WORLD!")

if __name__ == "__main__":
  register()

  # test call
  bpy.ops.import_mesh.lidar('INVOKE_DEFAULT')