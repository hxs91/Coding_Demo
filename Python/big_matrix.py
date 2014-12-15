#encoding=utf-8
'''
Created on Dec 12, 2014

@Author: admiral

@Description: 大矩阵乘法，将矩阵存储在文件中，通过类的封装实现一些操作。
'''

import os 
import struct

class Matrix:
    '实现大数据的矩阵乘法'
    def __init__(self,matrix_name,row,col,path='./big_matrix/',replace=False):
        self.path=path   #矩阵的存储目录
        self.mname=matrix_name
        self.row=row
        self.col=col
        self.nrow=range(row)
        self.ncol=range(col)
        if not os.path.exists(self.path):   #如果目录不存在，创建该目录
            os.mkdir(path)
        
        #如果文件不存在或者replace被置为True，创建并初始化该文件
        if not os.path.exists(self.path+self.mname) or replace:
            self.self_initialize()
    
    def add_row(self,cnt,rl):
        'cnt代表这是第几行(从0开始)，rl是一个list'
        if len(rl) != self.col:
            print 'column value does not match.'
            return None
        fobj=open(self.path+self.mname,'rb+')
        ss=''
        for x in rl:
            ss+=struct.pack('d',x)
        fobj.seek(cnt*self.col*struct.calcsize('d'),0)
        fobj.write(ss)
        fobj.close()
    
    def get_kth_row(self,k):
        '取出该矩阵的第k行'
        if k>self.row or k<1:
            print 'error occur in the value of k.'
            return None
        fobj=open(self.path+self.mname,'rb')
        fobj.seek((k-1)*self.col*struct.calcsize('d'),0) #定位文件指针的位置
        oneline = list( struct.unpack(str(self.col)+'d',fobj.read( self.col*struct.calcsize('d') ) ) )
        fobj.close()
        return oneline  #都用double类型来处理吧
                
    def get_kth_column(self,k):
        '取出该矩阵的第k列'
        if k>self.col:
            print 'error occur in the value of k.'
            return None
        rst=list()
        fobj=open(self.path+self.mname,'rb')
        for i in self.nrow:
            fobj.seek( i*self.col*struct.calcsize('d'),0)
            fobj.seek( (k-1)*struct.calcsize('d'),1 )
            data,=struct.unpack( 'd',fobj.read( struct.calcsize('d') ) )
            rst.append(data)
        fobj.close()
        return rst
    
    def mult(self,another,rstname):
        'self矩阵与another矩阵相乘，结果存放在rstname这个矩阵文件中'
        if self.col != another.row:
            print 'column and row number do not match.'
            return None
        rst=Matrix(rstname,self.row,another.col)
        for i in self.nrow:
            tmp=list()
            for j in another.ncol:
                ri=self.get_kth_row(i+1)
                cj=another.get_kth_column(j+1)
                value=sum([ vi*vj for (vi,vj) in zip(ri,cj) ])
                tmp.append(value)
            rst.add_row(i,tmp)
        return rst
    
    def update_value(self,i,j,val):
        '设置self[i][j]的值为val'
        if i<0 or i>=self.row or j<0 or j>=self.col:
            print 'wrong value for i and j.'
            return None
        fobj=open(self.path+self.mname,'rb+')
        fobj.seek( i*self.col*struct.calcsize('d')+j*struct.calcsize('d'),0 )
        fobj.write( struct.pack('d',val) )
        fobj.close()
        
    def get_value(self,i,j):
        '获取self[i][j]的值'
        if i<0 or i>=self.row or j<0 or j>=self.col:
            print 'wrong value for i and j.'
            return None
        fobj=open(self.path+self.mname,'rb')
        fobj.seek( i*self.col*struct.calcsize('d')+j*struct.calcsize('d'),0 )
        value,= struct.unpack( 'd',fobj.read( struct.calcsize('d') ) )
        return value
    
    def self_initialize(self):
        '将矩阵所有元素都初始化为0'
        fobj=open(self.path+self.mname,'wb')
        for i in self.nrow:
            ss=''
            for j in self.ncol:
                ss+=struct.pack('d',0)
            fobj.write(ss)
        fobj.close()
        
    def delete_matrix(self):
        if not os.path.exists(self.path+self.mname):
            print 'matrix dose not exist.'
            return None
        os.remove(self.path+self.mname)
        
if __name__ == '__main__':
    tmp=Matrix('boolmap',2963+3738+65142+1,2963+3738+65142+1)
    x=tmp.get_kth_row(4314)
    for t in x:
        if t!=0.0:
            print t