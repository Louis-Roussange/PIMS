#!/usr/bin/env python
import itertools
import Bio.PDB as pdb
import numpy as np
import gudhi
import plotly.graph_objects as go

from tp_pims.config import TP_PATH
from gudhi import DelaunayCechComplex
from Bio.PDB.Residue import Residue


def make_sphere(x: float, y: float, z: float, radius: float, resolution: int = 100):
    """Return the coordinates for plotting a sphere centered at (`x`,`y`,`z`) with radius `r`"""
    u, v = np.mgrid[0 : 2 * np.pi : resolution * 2j, 0 : np.pi : resolution * 1j]
    X = radius * np.cos(u) * np.sin(v) + x
    Y = radius * np.sin(u) * np.sin(v) + y
    Z = radius * np.cos(v) + z
    return (X, Y, Z)


def get_filtrations_values(simplex_tree: gudhi.SimplexTree):
    """Return filtration values when a simplice is aded to the complex."""
    filtration_values = []
    last_filtration = None
    for _, filtration in simplex_tree.get_filtration():
        if last_filtration != filtration:
            filtration_values.append(filtration)
            last_filtration = filtration
    print(len(filtration_values))
    return filtration_values


def draw_cech_balls(points: list, simplex_tree: gudhi.SimplexTree, wait: bool = True):
    """Draw Cech balls for each filtation values."""
    for filtration in get_filtrations_values(simplex_tree):
        spheres = []
        import math

        for point in points:
            (sphere_x, sphere_y, sphere_z) = make_sphere(
                x=point[0], y=point[1], z=point[2], radius=math.sqrt(filtration)
            )
            spheres.append(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, opacity=1))
        fig = go.Figure(data=spheres)
        fig.show()
        if wait:
            input()

def draw_ca_balls(points: list, simplex_tree: gudhi.SimplexTree, wait: bool = True):
    """Draw the first Cech balls radius = min(filtrations)."""
    filtration0 = min(get_filtrations_values(simplex_tree))
    spheres = []
    import math

    for point in points:
        (sphere_x, sphere_y, sphere_z) = make_sphere(
           x=point[0], y=point[1], z=point[2], radius=math.sqrt(filtration0)
        )
        spheres.append(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, opacity=1))
    fig = go.Figure(data=spheres)
    fig.show()
    if wait:
        input()



def get_complexes_filtration(simplex_tree: gudhi.simplex_tree):
    """Return all simplicial complexes encounter during the filtration."""
    last_filtration = None
    complexes = []
    complexe = []
    for simplice, filtration_value in simplex_tree.get_filtration():
        if last_filtration is None:
            last_filtration = filtration_value
        if filtration_value != last_filtration:
            complexes.append(list(complexe))
            last_filtration = filtration_value
        complexe.append(simplice)
    complexes.append(complexe)
    print(len(complexes))
    return complexes


def draw_simplicial_complex(
    points: list, simplicial_complex: gudhi.SimplexTree, wait: bool = True
):
    """Draw a simplicial complex."""
    for simplicial_complex in get_complexes_filtration(simplicial_complex):
        tetras = []
        triangles = []
        edges = []
        vertices = []
        for simplice in simplicial_complex:
            if len(simplice) == 1:
                vertices.append(simplice[0])
            if len(simplice) == 2:
                edges.append(simplice)
            elif len(simplice) == 3:
                triangles.append(simplice)
            elif len(simplice) == 4:
                tetras.append(simplice)

        point_vertices = np.array(
            [point for i, point in enumerate(points) if i in vertices]
        )

        f_triangles = go.Mesh3d(
            x=point_vertices[:, 0],
            y=point_vertices[:, 1],
            z=point_vertices[:, 2],
            i=[triangle[0] for triangle in triangles],
            j=[triangle[1] for triangle in triangles],
            k=[triangle[2] for triangle in triangles],
            color="cyan",
        )
        f_points = go.Scatter3d(
            x=point_vertices[:, 0],
            y=point_vertices[:, 1],
            z=point_vertices[:, 2],
            mode="markers",
            marker=dict(size=12, color=["orange" for _ in range(len(point_vertices))]),
        )

        data = [f_triangles, f_points]
        for tetra in tetras:
            tetra_faces = list(itertools.combinations(tetra, 3))
            data.append(
                go.Mesh3d(
                    x=point_vertices[:, 0],
                    y=point_vertices[:, 1],
                    z=point_vertices[:, 2],
                    i=[tetra_face[0] for tetra_face in tetra_faces],
                    j=[tetra_face[1] for tetra_face in tetra_faces],
                    k=[tetra_face[2] for tetra_face in tetra_faces],
                    color="blue",
                )
            )

        for edge in edges:
            pts = np.array([points[i] for i in edge])
            seg = go.Scatter3d(
                x=pts[:, 0],
                y=pts[:, 1],
                z=pts[:, 2],
                mode="lines",
                line=dict(color="pink", width=10),
            )
            data.append(seg)
        fig = go.Figure(data=data, layout=dict(showlegend=False))
        fig.show()
        if wait:
            input()


def extract_ca_atom_pos(aa_list: list[Residue]) -> list:
    """Extract CA position from a list of amino acids constructed with biopython."""
    ca = []
    for aa in aa_list:
        for atom in aa.get_atoms():
            atom_full_name = atom.fullname.replace(" ", "")
            if atom_full_name == "CA":
                ca.append(atom.coord)
                continue
    return ca


if __name__ == "__main__":
    path = str(TP_PATH / "script_pymol.py")
    parser = pdb.PDBParser(PERMISSIVE=1)
    protein = parser.get_structure(
        id=0, file=(TP_PATH / "data" / "AF-Q8U442-F1-model_v6.pdb").open("r")
    )
    alpha_helix_pos = [31, 36]
    alpha_helix_aa = list(protein.get_residues())[
        alpha_helix_pos[0] : alpha_helix_pos[1]
    ]
    pos_ca = extract_ca_atom_pos(alpha_helix_aa)
    cech_cs = DelaunayCechComplex(points=pos_ca)
    cech_simplex_tree_sample = cech_cs.create_simplex_tree()
    cech_barcode = cech_simplex_tree_sample.persistence()
    print(pos_ca)
    draw_cech_balls(pos_ca, cech_simplex_tree_sample)
    # draw_simplicial_complex(pos_ca, cech_simplex_tree_sample)
