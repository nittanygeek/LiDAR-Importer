# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "LiDAR-Tools",
    "author" : "Brian Hynds",
    "description" : "Import LiDAR",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Import-Export"
}

from . import auto_load

import bpy
import os
import sys
import subprocess
from pathlib import Path

from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator

py_path = Path(sys.prefix) / "bin"
py_exec = next(py_path.glob("python*"))
subprocess.call([str(py_exec), "-m", "ensurepip"])
subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "laspy"])

import laspy
import numpy as np
from laspy.file import File

auto_load.init()

class OT_LiDARImportFileBrowser(Operator,ImportHelper):
    bl_idname = "import_mesh.lidar"
    bl_label = "Import LiDAR file"
    filter_glob = StringProperty(
        default='*.las;*.laz', 
        options={'HIDDEN'}
    )

    def execute(self, context):

        filename, extension = os.path.splitext(self.filepath)

        return importLidarDataToScene(context, self.filepath)

# Menu Item for File > Import
def menu_func_import(self, context):
    self.layout.operator(OT_LiDARImportFileBrowser.bl_idname, text="LiDAR Format (.las/.laz)")

# Main Import Function (this is where the magic happens):
def importLidarDataToScene(context, filepath):

    # Get a reference to the scene
    scn = bpy.context.scene

    # Create a new mesh
    me = bpy.data.meshes.new("LiDARMesh")

    # Create a new object with the mesh
    obj = bpy.data.objects.new("LiDARObj", me)

    # Link the object to the scene
    scn.collection.objects.link(obj)

    # Read the file
    inFile = File(filepath, mode = "r")

    # Get all the points
    point_records = inFile.points

    # X,Y,Z Coords Array
    coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

    # Update the Mesh
    me.from_pydata(coords,[],[])
    me.update()

    # Center to Origin
    obj.select_set(True)
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

    # Close the File
    inFile.close()

    return {'FINISHED'}

def register():
    auto_load.register()
    bpy.utils.register_class(OT_LiDARImportFileBrowser)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    auto_load.unregister()
    bpy.utils.unregister_class(OT_LiDARImportFileBrowser)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
    
    # test call 
    bpy.ops.import_mesh.lidar('INVOKE_DEFAULT')