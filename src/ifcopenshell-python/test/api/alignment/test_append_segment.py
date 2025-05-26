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

import pytest
import ifcopenshell.api.alignment
import ifcopenshell.api.context
import math


def test_append_segment():
    file = ifcopenshell.file(schema="IFC4X3_ADD2")
    project = file.createIfcProject(Name="Test")
    geometric_representation_context = ifcopenshell.api.context.add_context(file, context_type="Model")
    axis_model_representation_subcontext = ifcopenshell.api.context.add_context(
        file,
        context_type="Model",
        context_identifier="Axis",
        target_view="MODEL_VIEW",
        parent=geometric_representation_context,
    )

    ali = ifcopenshell.api.alignment.create_alignment(file,"A1")
    horizontal_alignment = ifcopenshell.api.alignment.get_horizontal_alignment(ali)

    design_parameters = file.create_entity(
        type="IfcAlignmentHorizontalSegment",
        StartTag=None,
        EndTag=None,
        StartPoint=file.createIfcCartesianPoint(Coordinates=((0.0, 0.0))),
        StartDirection=0.0,
        StartRadiusOfCurvature=0.0,
        EndRadiusOfCurvature=0.0,
        SegmentLength=100.0,
        GravityCenterLineHeight=None,
        PredefinedType="LINE",
    )

    next_design_parameters = ifcopenshell.api.alignment.append_segment(file,horizontal_alignment,design_parameters)
    ifcopenshell.api.alignment.util.print_alignment(horizontal_alignment)
    assert len(horizontal_alignment.IsNestedBy) == 2

    next_design_parameters.SegmentLength = 50.0
    next_design_parameters.StartDirection=math.pi()/6

    next_design_parameters = ifcopenshell.api.alignment.append_segment(file,horizontal_alignment,next_design_parameters)
    ifcopenshell.api.alignment.util.print_alignment(horizontal_alignment)
    assert len(horizontal_alignment.IsNestedBy) == 3
