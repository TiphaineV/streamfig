for i in examples/*.py;
do
    name=$(basename $i .py);
    echo $name
    python3 ./examples/$name.py > $name.fig; fig2dev -Lpng $name.fig > ./examples/$name.png;
done
rm *.fig
