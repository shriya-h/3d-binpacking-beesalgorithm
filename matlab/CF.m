function p_length=CF(beepos,bin,boxes)

p_length=0;
l_n=length(boxes);
for i=1:l_n-1
s_length=setdiff(beepos(i),beepos(i+1));
p_length=p_length+s_length;
end
p_length=p_length+setdiff(beepos(l_n),beepos(1));
end