clc
clear all
close all

x=[-2 -1 2 3]';
y=[12.13533528 6.367879441  -4.610943901  2.085536923]';

A=[x.^3 x.^2 x ones(4,1)]
b=y;
a=inv(A)*b

xpol=-2:0.01:3;
p=a(1)*xpol.^3+a(2)*xpol.^2+a(3)*xpol+a(4);

plot(x,y,'r*',xpol,p,'b-')
hold on
grid on