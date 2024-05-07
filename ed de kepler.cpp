#include <iostream>
#include <cmath>
#include <fstream>
#define l 0.0
#define m 1.0
#define k -1.0
#define b 0.0
#define Pi 3.1416
using namespace std;

// Definición de las funciones f(x, y) y g(x, y)
double dxdt(double x, double y) {
    return y;  // Aquí define tu función f(x, y)
}

double dydt(double x, double y) {
    return pow(l/(m),2)*pow(1/x,3) +(k/m)*pow(1/x,2)-(b/m)*y;  // Aquí define tu función g(x, y)
}

double dzdt(double z,double x){
	return (l/m)*pow(1/x,2);
}

// Método de Euler para un sistema de ecuaciones diferenciales 2x2
void euler(double x0, double y0,double z0, double h, double t_final) {
	ofstream messi; 
	messi.open("Datos_Ed.dat");
	
    double x = x0;
    double y = y0;
    double z= z0;
    double t = 0.0;

    while (t < t_final) {
        // Imprime los valores actuales de x, y y t
        messi << t <<"  "<< x <<" "<< z << endl;

        // Calcula los nuevos valores de x e y usando el método de Euler
        double x_nuevo = x + h * dxdt(x, y);
        double y_nuevo = y + h * dydt(x, y);
        double z_nuevo = z + h*dzdt(z,x);

        // Actualiza los valores de x, y y t
        x = x_nuevo;
        y = y_nuevo;
        z= z_nuevo;
        t += h;
    }
}

int main() {
    // Parámetros iniciales
    double x0 = 1.0;   // Valor inicial de x
    double y0 =0.0;   // Valor inicial de y
    double z0=Pi/2;
    double h = 0.1;    // Tamaño del paso
    double t_final = 200.0;  // Tiempo final

    // Llama al método de Euler
    euler(x0, y0,z0, h, t_final);

    return 0;
}

