#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

int main() {
    // Parámetros configurables
    const int N_c = 2;  // 2 clusters (0 y 1)
    const double epsilon = 1e-4;
    const char* input_file = "vectorized_images.csv";
    const char* output_file = "clustered_results.csv";

    // Leer datos desde CSV
    ifstream dskr(input_file);
    if (!dskr.is_open()) {
        cerr << "Error: No se pudo abrir " << input_file << endl;
        return 1;
    }

    // Determinar dimensiones del dataset
    int N_data = 0;
    int D = 0;  // Dimensión de los vectores
    string line;
    while (getline(dskr, line)) {
        if (!line.empty()) {
            N_data++;
            if (D == 0) {
                stringstream ss(line);
                string value;
                while (getline(ss, value, ',')) {
                    D++;
                }
            }
        }
    }
    dskr.clear();
    dskr.seekg(0);

    // Almacenar datos
    vector<vector<double>> Data(N_data, vector<double>(D));
    for (int i = 0; i < N_data; i++) {
        string line;
        getline(dskr, line);
        stringstream ss(line);
        string value;
        for (int j = 0; j < D; j++) {
            getline(ss, value, ',');
            Data[i][j] = stod(value);
        }
    }
    dskr.close();

    // Inicialización de centroides
    vector<vector<double>> K(N_c, vector<double>(D));
    srand(time(NULL));
    for (int i = 0; i < N_c; i++) {
        for (int j = 0; j < D; j++) {
            K[i][j] = static_cast<double>(rand()) / RAND_MAX;  // [0, 1]
        }
    }

    // Variables para clustering
    vector<int> cluster(N_data, 0);
    double dist;
    int iter = 0;
    const int max_iter = 100;

    // Archivo de resultados
    ofstream dskw(output_file);
    dskw << "indice,cluster,digito\n";

    // Algoritmo k-means
    do {
        // Paso 1: Asignación de clusters
        for (int i = 0; i < N_data; i++) {
            double min_dist = 1e10;
            int best_cluster = 0;
            
            for (int j = 0; j < N_c; j++) {
                double d = 0.0;
                for (int k = 0; k < D; k++) {
                    double diff = Data[i][k] - K[j][k];
                    d += diff * diff;  // Distancia euclidiana al cuadrado
                }
                
                if (d < min_dist) {
                    min_dist = d;
                    best_cluster = j;
                }
            }
            cluster[i] = best_cluster;
        }

        // Paso 2: Actualización de centroides
        vector<vector<double>> new_K(N_c, vector<double>(D, 0.0));
        vector<int> counts(N_c, 0);
        
        for (int i = 0; i < N_data; i++) {
            int c = cluster[i];
            counts[c]++;
            for (int j = 0; j < D; j++) {
                new_K[c][j] += Data[i][j];
            }
        }
        
        for (int i = 0; i < N_c; i++) {
            if (counts[i] > 0) {
                for (int j = 0; j < D; j++) {
                    new_K[i][j] /= counts[i];
                }
            }
        }

        // Calcular desplazamiento de centroides
        dist = 0.0;
        for (int i = 0; i < N_c; i++) {
            for (int j = 0; j < D; j++) {
                double diff = K[i][j] - new_K[i][j];
                dist += diff * diff;
            }
        }
        dist = sqrt(dist);
        
        K = new_K;
        iter++;
    } while (dist > epsilon && iter < max_iter);

    // Paso 3: Asignar dígitos según intensidad
    vector<double> avg_intensity(N_c, 0.0);
    for (int i = 0; i < N_data; i++) {
        int c = cluster[i];
        for (double val : Data[i]) {
            avg_intensity[c] += val;
        }
    }
    
    // Calcular intensidad promedio por cluster
    for (int i = 0; i < N_c; i++) {
        avg_intensity[i] /= (N_data * D);
    }

    // Mapear clusters a dígitos
    vector<int> cluster_to_digit(N_c);
    if (avg_intensity[0] > avg_intensity[1]) {
        cluster_to_digit[0] = 1;
        cluster_to_digit[1] = 0;
    } else {
        cluster_to_digit[0] = 0;
        cluster_to_digit[1] = 1;
    }

    // Guardar resultados
    for (int i = 0; i < N_data; i++) {
        dskw << i << "," << cluster[i] << "," << cluster_to_digit[cluster[i]] << "\n";
    }
    dskw.close();

    cout << "Clustering completado en " << iter << " iteraciones\n";
    cout << "Resultados guardados en: " << output_file << endl;

    return 0;
}