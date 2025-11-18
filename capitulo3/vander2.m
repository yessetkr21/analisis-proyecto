clc
clear all
close all

x=[1.8 2 3 4 5]';
y=exp(-x/1.8)+1./(x.^2-3)

A=[x.^4 x.^3 x.^2 x ones(5,1)]
b=y;
a=inv(A)*b

xpol=1.8:0.01:5;
xpol2=1.8:0.01:5;
xpol1=1.8:0.01:5;
p=a(1)*xpol.^4+a(2)*xpol.^3+a(3)*xpol.^2+a(4)*xpol+a(5);
freal=exp(-xpol1/1.8)+1./(xpol1.^2-3);
freal2=exp(-xpol2/1.8)+1./(xpol2.^2-3);
plot(x,y,'r*',xpol,p,'b-')
hold on
grid on
Error1=abs(a(1)*2.5.^4+a(2)*2.5.^3+a(3)*2.5.^2+a(4)*2.5+a(5)-(exp(-2.5/1.8)+1./(2.5.^2-3)))
Error2=abs(a(1)*6.^4+a(2)*6.^3+a(3)*6.^2+a(4)*6+a(5)-(exp(-6/1.8)+1./(6.^2-3)))
plot(xpol1,freal,'c--', xpol2,freal2,'c--')