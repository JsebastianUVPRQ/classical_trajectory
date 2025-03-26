clear all, clc
state = uint64(1);
state = bitshift(state,31);
fprintf([dec2bin(state,64),'\n']);

for i=1:32
    r = bitor(state,bitshift(state,1));
    rn = bitxor(r,bitsrl(state,1));

    fprintf([dec2bin(rn,64),'\n']);
    state = rn;
end