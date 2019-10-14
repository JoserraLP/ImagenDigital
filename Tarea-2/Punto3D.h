#ifndef PUNTO3D_H_
#define PUNTO3D_H_

class Punto3D {
	int x,y,z;

public:
	Punto3D();
	~Punto3D();
	Punto3D(int x,int y, int z);
	int getX();
	void setX(int x);
	int getY();
	void setY(int y);
	int getZ();
	void setZ(int z);
};

#endif /* PUNTO3D_H_ */
