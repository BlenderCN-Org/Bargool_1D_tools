# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy
import math
from . import instances


class ImportCleanupOperator(bpy.types.Operator):
    """ Class by Paul Kotelevets, and my little edits """
    bl_idname = 'mesh.import_cleanup'
    bl_label = 'Obj Import Cleanup'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        objects = [o for o in context.selected_objects if
                   o.type == 'MESH' and o.is_visible(scene)]
        for ob in objects:
            ob.select = True
            context.scene.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            settings = context.scene.batch_operator_settings
            if settings.import_cleanup_remove_doubles:
                threshold = settings.import_cleanup_remove_doubles_threshold
                bpy.ops.mesh.remove_doubles(threshold=threshold, use_unselected=False)
            if settings.import_cleanup_tris_to_quads:
                limit = math.radians(settings.import_cleanup_tris_to_quads_limit)
                bpy.ops.mesh.tris_convert_to_quads(limit=limit, uvs=False,
                                                   vcols=False, sharp=False,
                                                   materials=False)
            do_recalculate_normals = settings.import_cleanup_recalculate_normals
            if do_recalculate_normals:
                bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            do_import_cleanup_apply_rotations = settings.import_cleanup_apply_rotations
            # transform_apply works only with non-multiuser
            if do_import_cleanup_apply_rotations and not instances.is_multiuser(ob):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        return {'FINISHED'}


def create_panel(col, scene):
    col.operator('mesh.import_cleanup')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_apply_rotations')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_recalculate_normals')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_remove_doubles')
    sub = col.row()
    sub.active = scene.batch_operator_settings.import_cleanup_remove_doubles
    sub.prop(scene.batch_operator_settings,
             'import_cleanup_remove_doubles_threshold',
             slider=True)
    col.prop(scene.batch_operator_settings,
             'import_cleanup_tris_to_quads')
    sub = col.row()
    sub.active = scene.batch_operator_settings.import_cleanup_tris_to_quads
    sub.prop(scene.batch_operator_settings,
             'import_cleanup_tris_to_quads_limit')