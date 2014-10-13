import bpy
import binascii
import struct
from liblas import file
from liblas import header
from liblas import color
import multiprocessing
import time
import bgl

# Blender Addon Information
# Used by User Preferences > Addons
bl_info = {
  "name" : "LiDAR Importer",
  "author" : "Brian C. Hynds, James Wright",
  "version" : (0, 1),
  "blender" : (2, 6, 0),
  "description" : "LiDAR File Importer with 3D Object Recognition",
  "category" : "Import-Export",
  "location" : "File > Import"
}

# Not In Use Yet: For implementing Multiprocessing Module
def worker(ImportLiDARData):
  print("")

# Not In Use Yet: For implementing Multiprocessing Module
def worker_complete(result):
  print("")

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
    bgl.glbegin()
    return read_lidar_data(context, self.filepath, self.pointCloudResolution, self.cleanScene)

# Addon GUI Panel
class LiDARPanel(bpy.types.Panel):
  """LiDAR Addon Panel"""
  bl_label = "LiDAR Addon"
  bl_space_type = "VIEW_3D"
  bl_region_type = "TOOLS"
  bl_category = "LiDAR Tools"

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
      obj.select = True
    bpy.ops.object.delete()

  # create a new mesh
  me = bpy.data.meshes.new("LidarMesh")

  # create a new object with the mesh
  obj = bpy.data.objects.new("LidarObject", me)

  # link the mesh to the scene
  scn.objects.link(obj)
  scn.objects.active = obj

  # Use this array for face construction if we decide to calculate them during import
  # faces = []

  # open the file
  f = file.File(filepath,mode='r')

  # lets get some header information from the file
  fileCount = f.header.count
  Xmax = f.header.max[0]
  Ymax = f.header.max[1]
  Zmax = f.header.max[2]

  Xmin = f.header.min[0]
  Ymin = f.header.min[1]
  Zmin = f.header.min[2]

  # use this value for limiting the maximum number of points.  Set to f.header.count for maximum.
  maxNumPoints = f.header.count

  # iterate through the point cloud and import the X Y Z coords into the array
  for p in f:
    if maxNumPoints > 0:
      coords.append((p.x-Xmin-((Xmax-Xmin)/2), p.y-Ymin-((Ymax-Ymin)/2), p.z-Zmin))
      maxNumPoints -= 1

    # Uncomment the following line for debugging purposes:
    # print("XYZ:", p.x, ",", p.y, ",", p.z)

  me.from_pydata(coords,[],[])
  me.update()

  # bpy.ops.object.mode_set(mode='EDIT', toggle=False)
  # bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

  print(str(fileCount) + " verticies in the LiDAR Point Cloud")

  print("Total time to process (seconds): ", time.time() - start_time)
  print("File: ", filepath)

  c = color.Color()
  print("Red: ", c.red)
  print("Green: ", c.green)
  print("Blue: ", c.blue)

  print("completed read_lidar_data...")
  print("Percentage of points imported: ", pointCloudResolution)

  context.area.header_text_set()

  return {'FINISHED'}

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
  self.layout.operator(ImportLiDARData.bl_idname, text="LiDAR Format (.las)")


def register():
  bpy.utils.register_class(ImportLiDARData)
  bpy.utils.register_class(LiDARPanel)
  bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
  bpy.utils.unregister_class(ImportLiDARData)
  bpy.utils.unregister_class(LiDARPanel)
  bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
  register()

  # test call
  bpy.ops.import_mesh.lidar('INVOKE_DEFAULT')
