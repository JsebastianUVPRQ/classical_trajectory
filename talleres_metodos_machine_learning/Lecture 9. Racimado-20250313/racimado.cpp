
int main() {
    FILE *dskr;
    int err, N_data=336;
    char FileName[100];
    err = sprintf(FileName, "data/racimado.dat");
    err++;
    diskr = fopen(FileName, "r");

    RealMatrix Data(N_data, 2);
    for (int i = 0; i < N_data; i++) {
        char data_x[20], data_y[20], data_z[10];
        err = fscanf(dskr, "%s %s %s", data_x, data_y, data_z);
        Real x,y,z;
        x = toDouble(data_x);
        y = toDouble(data_y);
        z = toDouble(data_z);
        z++;
        Data(i, 0) = x;
        Data(i, 1) = y;
    }
    fclose(dskr);

    int cluster[N_data];
    Real dist,epsilon = 1e-4;
    RealMatrix K(N_c,2);
    strand (time(NULL));
    for (int i = 0; i < N_c; i++) {
        K(i, 0) = 300.*rand()%10000 / 10000.0+400;
        K(i, 1) = 300.*rand()%10000 / 10000.0+200;
    }

    FILE *dskw;;
    dskw = fopen("data/racimado_kmeans.dat", "w");
    do {
        RealVector Dkr(3);
        for (int i = 0; i < N_data; i++) {
            for (int j = 0; j < N_c; j++) {
                Dkr(j) = sqrt(pow(Data(i, 0) - K(j, 0), 2) + pow(Data(i, 1) - K(j, 1), 2));
            if (Dkr(0) < Dkr(1))
                if (Dkr(2) < Dkr(0))
                    cluster[i] = 2;
                else
                    cluster[i] = 0;
            else
                if (Dkr(2) < Dkr(1))
                    cluster[i] = 2;
                else
                    cluster[i] = 1;
            }
            Realmatrix K_new(N_c, 2);
            int N_p[N_c];
            N_p[0] = 0;
            N_p[1] = 0;
            N_p[2] = 0;
            for (int i = 0; i < N_data; i++) {
                K_new(cluster[i], 0) += Data(i, 0);
                K_new(cluster[i], 1) += Data(i, 1);
                N_p[cluster[i]]++;
            }
            for (int i = 0; i < N_c; i++) {
                if (N_p[i] != 0) {
                    K_new(i, 0) /= N_p[i];
                    K_new(i, 1) /= N_p[i];
                }
            dist = 0.;
            for (int i = 0; i < N_c; i++) {
                dist += sqrt(pow(K_new(i, 0) - K(i, 0), 2) + pow(K_new(i, 1) - K(i, 1), 2));
                fprintf(dskw, "%g %g\n", K_new(i, 0), K_new(i, 1));
            }
            fprintf(dskw, "\n");
            fflush(dskw);
            K = K_new;
        }while(dist > epsilon);
        fclose(dskw);
    }
}
}