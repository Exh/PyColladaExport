#!/usr/bin/env python

import sys
sys.path.append("pycollada")
import collada
import numpy
import sys
import math
from collada.util import normalize_v3

# command line arguments 1 - input collada path; 2 - output CSV path

class ColladaParser:
	def __init__(self, inFileName):
	# 	inputFilename = sys.argv[1]
		col = collada.Collada(inFileName, ignore=[collada.DaeUnsupportedError, collada.DaeBrokenRefError])
		if col.scene is not None:
			for geom in col.scene.objects('geometry'):
				for prim in geom.primitives():
					# use primitive-specific ways to get triangles
					prim_type = type(prim).__name__
					if prim_type == 'BoundTriangleSet':
						triangles = prim										
					elif prim_type == 'BoundPolylist':
						triangles = prim.triangleset()
					else:
						print 'Unsupported mesh used:', prim_type
						triangles = None					
					if triangles is not None:							
	
						# # triangles.generateNormals()								
						vertices = triangles.vertex #.flatten().tolist()						
						vertex_indices = triangles.vertex_index #.flatten().tolist()							
						VERTICES = vertices[vertex_indices]		
						
						normals = triangles.normal					
						normal_indices = triangles.normal_index # .flatten().tolist()
						NORMALS = normals[normal_indices]					
	

						uv = triangles.texcoordset[0]
						uv_indices = triangles.texcoord_indexset[0]
						UV = uv[uv_indices]
						
						x1 = VERTICES[:,1,0] - VERTICES[:,0,0]
						x2 = VERTICES[:,2,0] - VERTICES[:,0,0]
						y1 = VERTICES[:,1,1] - VERTICES[:,0,1]
						y2 = VERTICES[:,2,1] - VERTICES[:,0,1]
						z1 = VERTICES[:,1,2] - VERTICES[:,0,2]
						z2 = VERTICES[:,2,2] - VERTICES[:,0,2]
	
						s1 = UV[:,1,0] - UV[:,0,0]
						s2 = UV[:,2,0] - UV[:,0,0]
						t1 = UV[:,1,1] - UV[:,0,1]
						t2 = UV[:,2,1] - UV[:,0,1]	       			
	
						f = 1.0 / (s1 * t2 - s2 * t1)
						tanX = (x1 * t2 - x2 * t1) * f
						tanY = (y1 * t2 - y2 * t1) * f
						tanZ = (z1 * t2 - z2 * t1) * f
					
						tangent = numpy.vstack((tanX, tanY, tanZ)).T					
						TANGENTS = normalize_v3(tangent)    			# one tangent   for triangle face				
						BINORMALS = numpy.cross(NORMALS, tangent)		# one BINORMALS for triangle face					
						self.VERTICES 	= VERTICES 	 
						self.NORMALS 	= NORMALS
						self.UV 		= UV
						self.TANGENTS 	= TANGENTS
						self.BINORMALS 	= BINORMALS

	def export(self, outFileName):
		VERTICES  = self.VERTICES 	  	 
		NORMALS   = self.NORMALS 	 
		UV        = self.UV 		
		TANGENTS  = self.TANGENTS 	
		BINORMALS = self.BINORMALS 									
		file = open(outFileName, "w")
		for i in range(0, len(VERTICES)):						
			v1 = ("%0.7f" % VERTICES[i][0][0], "%0.7f" % VERTICES[i][0][1], "%0.7f" % VERTICES[i][0][2], "%0.7f" % NORMALS[i][0][0], "%0.7f" % NORMALS[i][0][1], "%0.7f" % NORMALS[i][0][2], "%0.7f" % TANGENTS[i][0], "%0.7f" % TANGENTS[i][1], "%0.7f" % TANGENTS[i][2], "%0.7f" % BINORMALS[i][0][0], "%0.7f" % BINORMALS[i][0][1], "%0.7f" % BINORMALS[i][0][2], "%0.7f" % UV[i][0][0], "%0.7f" % UV[i][0][1])
			v2 = ("%0.7f" % VERTICES[i][1][0], "%0.7f" % VERTICES[i][1][1], "%0.7f" % VERTICES[i][1][2], "%0.7f" % NORMALS[i][1][0], "%0.7f" % NORMALS[i][1][1], "%0.7f" % NORMALS[i][1][2], "%0.7f" % TANGENTS[i][0], "%0.7f" % TANGENTS[i][1], "%0.7f" % TANGENTS[i][2], "%0.7f" % BINORMALS[i][1][0], "%0.7f" % BINORMALS[i][1][1], "%0.7f" % BINORMALS[i][1][2], "%0.7f" % UV[i][1][0], "%0.7f" % UV[i][1][1])
			v3 = ("%0.7f" % VERTICES[i][2][0], "%0.7f" % VERTICES[i][2][1], "%0.7f" % VERTICES[i][2][2], "%0.7f" % NORMALS[i][2][0], "%0.7f" % NORMALS[i][2][1], "%0.7f" % NORMALS[i][2][2], "%0.7f" % TANGENTS[i][0], "%0.7f" % TANGENTS[i][1], "%0.7f" % TANGENTS[i][2], "%0.7f" % BINORMALS[i][2][0], "%0.7f" % BINORMALS[i][2][1], "%0.7f" % BINORMALS[i][2][2], "%0.7f" % UV[i][2][0], "%0.7f" % UV[i][2][1])						
			faceStr = 			''.join('%s, ' % x for x in v1[:-1]) + v1[-1] + "\n"
			faceStr = faceStr + ''.join('%s, ' % x for x in v2[:-1]) + v2[-1] + "\n"
			faceStr = faceStr + ''.join('%s, ' % x for x in v3[:-1]) + v3[-1] + "\n"						
			file.write(faceStr)							
		file.close()	

if len(sys.argv) > 2:
	parser = ColladaParser(sys.argv[1])
	parser.export(sys.argv[2])
		# exit(0)
else:
	exit(1)
