bl_info = {
    'name': 'EASIER',
    'author': 'Ömer Faruk Genç',
    'description': "This addon was written to be able to operate in Blender faster and easier.",
    'blender': (3, 6),
    'version': (1, 2),
    'location': 'View3D > Sidebar > EASIER',
    'warning': '',
    'wiki_url': "",
    'tracker_url': "",
    'category': 'Interface'
}

import bpy
from bpy.props import EnumProperty, StringProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup
from bpy.utils import register_class, unregister_class
from . import addon_updater_ops

global action_name
class Action_Editor_Settings(Panel):
    bl_idname = 'PT_action_editor_settings'
    bl_label = "Action Editor Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EASIER"
 
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        
        layout.operator('id.delete_all_actions', text='Delete All Actions', icon= "COLLAPSEMENU")
        
        layout.operator('id.delete_actions', text='Delete Unprotected Actions', icon= "FAKE_USER_OFF")
        
        for i in range(3):
            row = layout.row()
        
        layout.operator('id.open_fake_user', text='Open All Fake Users', icon= "FAKE_USER_ON")
        
        for i in range(3):
            row = layout.row()
            
        mytool = context.scene.my_tool
        
        layout.prop(mytool, "action_name")
        
        layout.operator('id.delete_action_by_name', text='Delete Action by Name', icon= "CANCEL")
        

class Delete_Actions(Operator):
    bl_idname = 'id.delete_actions'
    bl_label = 'Delete Actions'

    def execute(self, context):
        actions = [act for act in bpy.data.actions]
        for action in actions:
            if bpy.data.actions[action.name].use_fake_user != True:
                bpy.data.actions.remove(action)
        
        return {'FINISHED'}

class Delete_All_Actions(Operator):
    bl_idname = 'id.delete_all_actions'
    bl_label = 'Delete All Actions'

    def execute(self, context):
        actions = [act for act in bpy.data.actions]
        for action in actions:
            bpy.data.actions.remove(action)
        
        return {'FINISHED'}
    
class Open_Fake_User(Operator):
    bl_idname = 'id.open_fake_user'
    bl_label = 'Fake User Ac'

    def execute(self, context):
        actions = [act for act in bpy.data.actions]
        for action in actions:
            action.use_fake_user = True
        
        return {'FINISHED'}
    
class ActionName(PropertyGroup):
    action_name: StringProperty(
    name="Name",
    description=":",
    default="",
    maxlen=64)
    
    
class Delete_Action_By_Name(Operator):
    bl_idname = 'id.delete_action_by_name'
    bl_label = 'Delete Action By Name'

    def execute(self, context):
        actions = [act for act in bpy.data.actions]
        action_name = bpy.context.scene.my_tool.action_name
        for action in actions:
            if action.name == action_name:
                bpy.data.actions.remove(action)
                break
        
        return {'FINISHED'}
    



class Outliner_Controls(Panel):
    bl_idname = 'PT_outliner_controls'
    bl_label = "Outliner Controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EASIER"
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        
        layout.operator("id.monitors", text = "Turn Off/On All Monitors", icon = "RESTRICT_VIEW_OFF")
        
        
        layout.operator("id.renders", text = "Turn Off/On All Renders", icon = "RESTRICT_RENDER_OFF")
        
        row = layout.row()
        row = layout.row()
        
        layout.operator("id.monitor_of_selected_close", text = "Turn Off Selected's Monitor", icon = "VIS_SEL_01")
        
        
        layout.operator("id.monitor_of_selected_open", text = "Turn On Selected's Monitor", icon = "VIS_SEL_11") 
        
class Monitors(Operator):
    bl_idname = 'id.monitors'
    bl_label = "Monitors"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.data.collections[0].hide_viewport == True:
            for collection in bpy.data.collections:
                bpy.data.collections[collection.name].hide_viewport = False
                for object in collection.objects:
                    object.hide_viewport = False
        else:
            for collection in bpy.data.collections:
                bpy.data.collections[collection.name].hide_viewport = True
                for object in collection.objects:
                    object.hide_viewport = True
        
        return {'FINISHED'}

class Renders(Operator):
    bl_idname = 'id.renders'
    bl_label = "Renders"
    
    def execute(self, context):
        layout = self.layout
        
        if bpy.data.collections[0].hide_render == True:
            for collection in bpy.data.collections:
                bpy.data.collections[collection.name].hide_render = False
                for object in collection.objects:
                    object.hide_render = False
        else:
            for collection in bpy.data.collections:
                bpy.data.collections[collection.name].hide_render = True
                for object in collection.objects:
                    object.hide_render = True
        
        return {'FINISHED'}
        
class Monitor_Of_Selected_Close(Operator):
    bl_idname = 'id.monitor_of_selected_close'
    bl_label = "Selected's Monitor Close"
    
    def execute(self, context):
        layout = self.layout
        
        global selection_names
        try:
            selection_names += bpy.context.selected_objects
        except:    
            selection_names = bpy.context.selected_objects
            
        for selected in selection_names:
            if (selected.hide_viewport != True):
                selected.hide_viewport = True
    
        return {'FINISHED'}
    
class Monitor_Of_Selected_Open(Operator):
    bl_idname = 'id.monitor_of_selected_open'
    bl_label = "Selected's Monitor Open"
    
    def execute(self, context):
        layout = self.layout
        
        global selection_names
        for selected in selection_names:
            if (selected.hide_viewport == False):
                selected.hide_viewport = True
            else:
                selected.hide_viewport = False
        
        selection_names = []
    
        return {'FINISHED'}

class DemoUpdaterPanel(bpy.types.Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "Updater Demo Panel"
    bl_idname = "OBJECT_PT_DemoUpdaterPanel_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    bl_context = "objectmode"
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout

        addon_updater_ops.check_for_update_background()

        layout.label(text="Demo Updater Addon")
        layout.label(text="")

        col = layout.column()
        col.scale_y = 0.7
        col.label(text="If an update is ready,")
        col.label(text="popup triggered by opening")
        col.label(text="this panel, plus a box ui")

        # Could also use your own custom drawing based on shared variables.
        if addon_updater_ops.updater.update_ready:
            layout.label(text="Custom update message", icon="INFO")
        layout.label(text="")

        # Call built-in function with draw code/checks.
        addon_updater_ops.update_notice_box_ui(self, context)


@addon_updater_ops.make_annotations
class DemoPreferences(bpy.types.AddonPreferences):
    """Demo bare-bones preferences"""
    bl_idname = __package__

    # Addon updater preferences.

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31)

    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    def draw(self, context):
        layout = self.layout
        
        # Works best if a column, or even just self.layout.
        mainrow = layout.row()
        col = mainrow.column()

        # Updater draw function, could also pass in col as third arg.
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # ops = col.operator("wm.url_open","Open webpage ")
        # ops.url=addon_updater_ops.updater.website


classes = (
    DemoPreferences,
    DemoUpdaterPanel
)
    


def register():
    register_class(Action_Editor_Settings)
    register_class(Delete_Actions)
    register_class(Delete_All_Actions)
    register_class(ActionName)
    register_class(Delete_Action_By_Name)
    bpy.types.Scene.my_tool = PointerProperty(type=ActionName)
    
    register_class(Open_Fake_User)
    register_class(Outliner_Controls)
    register_class(Renders)
    register_class(Monitors)
    register_class(Monitor_Of_Selected_Close)
    register_class(Monitor_Of_Selected_Open)

    addon_updater_ops.register(bl_info)
    for cls in classes:
       addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
       bpy.utils.register_class(cls)

    
    

def unregister():
    unregister_class(Action_Editor_Settings)
    unregister_class(Delete_Actions)
    unregister_class(Delete_All_Actions)
    unregister_class(Open_Fake_User)
    unregister_class(ActionName)
    register_class(Delete_Action_By_Name)
    
    unregister_class(Outliner_Controls)
    unregister_class(Renders)
    unregister_class(Monitors)
    unregister_class(Monitor_Of_Selected_Close)
    unregister_class(Monitor_Of_Selected_Open)

    addon_updater_ops.unregister()
    for cls in reversed(classes):
       bpy.utils.unregister_class(cls)
 
if __name__ == '__main__':
    register()
