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
#import ifcopenshell.api.alignment.create_alignment
import ifcopenshell.api.alignment.get_alignment_segments
import ifcopenshell.api.context


def test_get_alignment():
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

    include_vertical = [False,True,True]
    include_cant = [False, False, True]
    expected_curve_type = ["IfcCompositeCurve","IfcGradientCurve","IfcSegmentedReferenceCurve","IfcSegmentedReferenceCurve"]

    for i in range(0,3) :
        ali = ifcopenshell.api.alignment.create_alignment(file,"A1",include_vertical[i],include_cant[i])
        assert ali != None

        curve = ifcopenshell.api.alignment.get_curve(ali)
        assert(curve.is_a() == expected_curve_type[i])
        assert len(curve.Segments) == 1
        assert ifcopenshell.api.alignment.has_zero_length_segment(curve)

        horiz = ifcopenshell.api.alignment.get_horizontal_alignment(ali)
        vert = ifcopenshell.api.alignment.get_vertical_alignment(ali)
        cant = ifcopenshell.api.alignment.get_cant_alignment(ali)

        assert ali == ifcopenshell.api.alignment.get_alignment(horiz)
        if include_vertical[i]:
            assert ali == ifcopenshell.api.alignment.get_alignment(vert)
        
        if include_cant[i]:
            assert ali == ifcopenshell.api.alignment.get_alignment(cant)
