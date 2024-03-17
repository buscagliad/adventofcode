#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  linalg.py
#  
#  Copyright 2024 Dave Buscaglia <dave@MintOS>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import random


class Vector3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	
	def dot(self, other):
		s = self.x * other.x + self.y * other.y + self.z * other.z
		return s
	def cross(self, other):
		x = self.y * other.z - self.z * other.y
		y = self.x * other.y - self.z * other.x
		z = self.x * other.y - self.y * other.x
		return Vector3(x, -y, z)
	def out(self, text=""):
		print(text, "Vector: ", self.x, self.y, self.z)
	def add(self, other):
		return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
	def sub(self, other):
		return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
		

class Matrix:
	def __init__(self, n):
		self.M = np.zeros([n,n], dtype = float)
	def setv(self, i, j, v):
		self.M[i][j] = v
	def setm(self, m):
		self.M = m
	def inv(self):
		m = np.linalg.inv(self.M)
		lm = Matrix(len(self.M[0]))
		lm.M = m
		return lm
	def solve(self, b):
		print("Xolve: ", b)
		x = np.linalg.solve(self.M, b)
		x.reshape(1,len(b))
		# print("Solve: ", x)
		# print("M", self.M)
		# print("M*x: ", self.vmult(x))
		# print("x: ", x)
		return x
	def mult(self, m):
		n = len(self.M[0])
		rm = Matrix(n)
		for i in range(n):
			for j in range(n):
				for k in range(n):
					rm.M[i][j] += self.M[i][k] * m.M[k][j]
		return rm
	def vmult(self, v):
		# print("vmult: ", v)
		n = len(self.M[0])
		rm = np.zeros(n).reshape(1, n)
		for i in range(n):
			for j in range(n):
				rm[0][i] += self.M[i][j] * v[j][0]
		return rm
	def out(self, text = ""):
		print(text)
		print(self.M)

def test():
	print("Top of test()")
	v = Vector3(3, -3, 1)
	v.out("v.out()")
	v2 = Vector3(4, 9, 2)
	v2.out("v2.out()")
	v3 = v.cross(v2)
	v3.out("v3.out()")
	print("v3.dot(v2): ", v3.dot(v2))
	print("v3.dot(v): ", v3.dot(v))
	m = Matrix(6)
	for i in range(6):
		for j in range(6):
			m.setv(i,j , random.random())
	
	m.out("Matrix M")
	MI = m.inv()
	MI.out("Matrix M inverse")
	mm = MI.mult(m)
	mm.out("Matrix M inverse * M (should be I)")
	
	A = np.array([[1, 9, 2, 1, 1],
				 [10, 1, 2, 1, 1],
				 [1, 0, 5, 1, 1],
				 [2, 1, 1, 2, 9],
				 [2, 1, 2, 13, 2]])
	b = np.array([170, 180, 140, 180, 350]).reshape((5, 1))
	x = np.linalg.solve(A, b)
	print(x)
	
	M = Matrix(5)
	for i in range(5):
		for j in range(5):
			M.setv(i, j, A[i][j])
	x = M.solve(b)
	print(x)
	
#test()
