# Description:

Iterate through a directory and add images missing to the start and end of the sequence using a template file to pad with. Useful for filling in CG sequences to save time on rendering.

# Args:

```
parser.add_argument('-i', '--input', type=str, required=True, help='Source directory')
parser.add_argument('-o', '--output', type=str, required=True, help='Output directory')
parser.add_argument('-f', '--filenameTemplate',required=True,  help='The filename template to use. Use # for the frame number')
parser.add_argument('-t', '--template', type=str, required=True, help='Template image to pad with')
parser.add_argument('-s', '--startFrame', type=int, default=1000, help='Start Frame')
parser.add_argument('-e', '--endFrame', type=int, default=1120, help='End Frame')
parser.add_argument('-z', '--zPadding', type=int, default=4, help='How many 0s to pad with')
```

# Usage:

```
python padImages.py  -i foam_01 -o foam_01b -f foam01_#.png -t foam_white.png -s 1000 -e 1120 -z 4
```



```
padImages.exe  -i foam_01 -o foam_01b -f foam01_#.png -t foam_white.png -s 1000 -e 1120 -z 4
```


