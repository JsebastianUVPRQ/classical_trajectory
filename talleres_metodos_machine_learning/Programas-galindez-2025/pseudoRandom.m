close all
n = 10000;
seed = 987986876876/8768768768987987;
r = 4;

x = zeros(1,n+1);
x(1) = seed;

for i=1:n
    x(i+1) = r*x(i)*(1-x(i));
end

plot(x)
figure
histogram(x)
