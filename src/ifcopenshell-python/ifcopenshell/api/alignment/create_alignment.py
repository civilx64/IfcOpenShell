# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2025 Thomas Krijnen <thomas@aecgeeks.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.

import ifcopenshell
import ifcopenshell.api.alignment
from ifcopenshell import entity_instance

def create_alignment(
    file: ifcopenshell.file,
    alignment_name: str,
    include_vertical: bool=False,
    include_cant: bool=False
) -> entity_instance:
    """
    Create an IfcAlignment, the corresponding IfcAlignmentHorizontal and ...

    :return: Returns an IfcAlignment
    """
    # create the alignment
    alignment = file.createIfcAlignment(
        GlobalId=ifcopenshell.guid.new(),
        Name=alignment_name,
    )

    alignment_layouts = []

    alignment_layouts.append(file.createIfcAlignmentHorizontal(GlobalId=ifcopenshell.guid.new()))

    if include_vertical :
        alignment_layouts.append(file.createIfcAlignmentVertical(GlobalId=ifcopenshell.guid.new()))

    if include_cant :
        alignment_layouts.append(file.createIfcAlignmentCant(GlobalId=ifcopenshell.guid.new(),RailHeadDistance=1.))

    # nest the horizontal and vertical under the alignment
    ifcopenshell.api.nest.assign_object(file, related_objects=alignment_layouts, relating_object=alignment)

    ifcopenshell.api.alignment.create_geometric_representation(file,alignment)


    # IFC 4.1.4.1.1 Alignment Aggregation To Project
    project = file.by_type("IfcProject")[0]
    ifcopenshell.api.aggregate.assign_object(file, products=[alignment], relating_object=project)

    return alignment
