#!/usr/bin/env python
import itertools

import numpy as np
import gudhi
import plotly.graph_objects as go

def make_sphere(x: float, y: float, z: float, radius: float, resolution: int=10):
    """Return the coordinates for plotting a sphere centered at (`x`,`y`,`z`) with radius `r`"""
    u, v = np.mgrid[0:2*np.pi:resolution*2j, 0:np.pi:resolution*1j]
    X = radius * np.cos(u)*np.sin(v) + x
    Y = radius * np.sin(u)*np.sin(v) + y
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

    return filtration_values

def draw_cech_balls(points: list, simplex_tree: gudhi.SimplexTree):
    """Draw Cech balls for each filtation values."""       
    for filtration in get_filtrations_values(simplex_tree):
        spheres = []
        for point in points:
            (sphere_x, sphere_y, sphere_z) = make_sphere(x=point[0], y=point[1], z=point[2], radius=filtration)
            spheres.append(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, opacity=0.5))
        fig = go.Figure(data=spheres)
        fig.show()

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
    return complexes

# # Coordinates of the points
# points=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,1],[1,1,0],[0,1,1]])
# # Build the simplicial complex with a tetrahedon, an edge and an isolated vertex
# cplx=gudhi.SimplexTree()
# cplx.insert([1,2,3,5])
# cplx.insert([4,6])
# cplx.insert([0])
# # List of triangles (point indices)
# triangles = np.array([s[0] for s in cplx.get_skeleton(2) if len(s[0])==3])
# print(triangles)
# # List of edges (point coordinates)
# edges = []
# for s in cplx.get_skeleton(1):
#     e = s[0]
#     if len(e) == 2:
#         edges.append(points[[e[0],e[1]]])

# ## With plotly
# import plotly.graph_objects as go
# # Plot triangles
# f2 = go.Mesh3d(
#         x=points[:,0],
#         y=points[:,1],
#         z=points[:,2],
#         i = triangles[:,0],
#         j = triangles[:,1],
#         k = triangles[:,2],
#     )
# # Plot points
# f0 = go.Scatter3d(x=points[:,0], y=points[:,1], z=points[:,2], mode="markers")
# data = [f2, f0]
# # Plot edges
# for pts in edges:
#     seg = go.Scatter3d(x=pts[:,0],y=pts[:,1],z=pts[:,2],mode="lines",line=dict(color='green'))
#     data.append(seg)
# fig = go.Figure(data=data,layout=dict(showlegend=False))
# # By default plotly would give each edge its own color and legend, that's too much
# fig.show()

def draw_simplicial_complex(points: list, simplicial_complex: gudhi.SimplexTree):
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


        point_vertices = np.array([point for i, point in enumerate(points) if i in vertices])

        f_triangles = go.Mesh3d(
            x=point_vertices[:,0],
            y=point_vertices[:,1],
            z=point_vertices[:,2],
            i = [triangle[0] for triangle in triangles],
            j = [triangle[1] for triangle in triangles],
            k = [triangle[2] for triangle in triangles],
            color="cyan"
        )
        f_points = go.Scatter3d(x=point_vertices[:,0], y=point_vertices[:,1], z=point_vertices[:,2], mode="markers", marker=dict(
            size=12,
            color=["orange" for _ in range(len(point_vertices))]))
        
        data = [f_triangles, f_points]
        for tetra in tetras:
            tetra_faces = list(itertools.combinations(tetra, 3))
            print(tetra_faces)
            data.append(go.Mesh3d(
                x=point_vertices[:,0],
                y=point_vertices[:,1],
                z=point_vertices[:,2],
                i = [tetra_face[0] for tetra_face in tetra_faces],
                j = [tetra_face[1] for tetra_face in tetra_faces],
                k = [tetra_face[2] for tetra_face in tetra_faces],
                color="blue"
            ))

        for edge in edges:
            pts = np.array([points[i] for i in edge])
            seg = go.Scatter3d(x=pts[:,0],y=pts[:,1],z=pts[:,2],mode="lines",line=dict(color='pink', width=10))
            data.append(seg)
        fig = go.Figure(data=data,layout=dict(showlegend=False))
        fig.show()

if __name__ == "__main__":
    points=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,1],[1,1,0],[0,1,1]])
    cplx=gudhi.SimplexTree()
    cplx.insert([1,2,3,5], filtration=0.8)
    cplx.insert([1,2,3], filtration=0.7)
    cplx.insert([4,6], filtration=0.5)
    cplx.insert([0], filtration=0.1)
    for simplicial_complex in get_complexes_filtration(cplx):
        draw_simplicial_complex(points, simplicial_complex)
