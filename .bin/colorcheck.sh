#!/bin/bash
# Terminal Color Viewer (only works on bash)


if [ $# -eq 0 ]; then
    esc="\033["
    name=("\t black" "\t red" "\t green" "\t yellow" "\t blue" "\t magenta" " cyan" "\t white")
    for b in {40..47}; do
        top1="${top1}\t ${esc}$(($b-10))m${b}"
        top2="${top2}${esc}$(($b-10))m${name[$(($b-40))]}"
    done
    echo -e "$top1\n$top2"

    for f in {30..37}; do
        line1="${esc}01;${f}m${f}${esc}0m\t" line2="\t"
        for b in {40..47}; do
            line1="${line1}${esc}${b};${f}m Normal ${esc}0m"
            line2="${line2}${esc}${b};${f};1m Bold \t${esc}0m"
        done
        echo -e "    $line1\n$line2"
    done
fi


#=============================================================================
# Color Alias
#=============================================================================
R="\033[1;31m"; r="\033[0;31m";
G="\033[1;32m"; g="\033[0;32m";
Y="\033[1;33m"; y="\033[0;33m";
B="\033[1;34m"; b="\033[0;34m";
M="\033[1;35m"; m="\033[0;35m";
C="\033[1;36m"; c="\033[0;36m";
n="\033[0m";


src_c="${c}// This is C sample code.
${m}#include ${y}<stdio.h> ${c}// printf
${m}#include ${y}<stdlib.h> ${c}// qsort

${m}#define ${y}SIZEOF(arr) (sizeof(arr) / sizeof(arr[0]))

${b}int${n} ${y}cmp${n}(${b}const void${n}* a, ${b}const void${n}* b) {
    ${B}return${n} ( *(${b}int${n}*)a - *(${b}int${n}*)b );
}

${b}int${n} ${y}main${n}(${b}int${n} argc, ${b}char${n}* argv[]) {
    ${b}int${n} nums[] = {${r}5${n}, ${r}2${n}, -${r}6${n}, -${r}1${n}, ${r}0${n}, -${r}3${n}, ${r}7${n}, ${r}9${n}};
    ${b}const int${n} LEN = ${m}SIZEOF${n}(nums);

    ${b}int${n} i;
    ${b}int${n} *p = nums;

    ${y}qsort${n}(nums, LEN, ${B}sizeof${n}(${b}int${n}), cmp);

    ${y}printf${n}(${g}\"Sorted array:\\\\n\\\\t[\"${n});
    ${B}for${n} (i=${r}0${n}; i<LEN; ++i) {
        ${y}printf${n}(${g}\"%d, \"${n}, *p);
        ++p;
    }
    ${y}printf${n}(${g}\"]; \\\\n\"${n});

    ${B}return${n} ${r}0${n};
}
"

src_py="${m}#!/usr/bin/python
# coding: utf-8${n}
${c}# This is a python code.

${B}def${n} ${y}qsort${n}(aList):
    ${g}\"\"\" 
        Return the sorted \`aList'.
        ${m}>>> lst = [4, 7, -8, 3, 6, 0, 9, -3, 8]
        >>> qsort(lst)
        [-8, -3, 0, 3, 4, 6, 7, 8, 9]${g}
    \"\"\"${n}
    ${B}if not${n} aList:
        ${B}return${n} aList
    ${B}else${n}:
        pivot = aList[${r}0${n}]
        less = [x ${B}for${n} x ${B}in${n} aList     ${B}if${n} x <  pivot]
        more = [x ${B}for${n} x ${B}in${n} aList[${r}1${n}:] ${B}if${n} x >= pivot]
        ${B}return${n} ${y}qsort${n}(less) + [pivot] + ${y}qsort${n}(more)

${B}if${n} ${m}__name__${n}==${g}'__main__'${n}:
    ${B}import${n} doctest
    doctest.${y}testmod${n}()
"

src_hs="${c}-- This is a Haskell code.${n}

${B}module${n} Main ${B}where${n}

qsort :: [${b}Int${n}] -> [${b}Int${n}]
qsort [] = []
qsort (x:xs) = before ++ (x : after)
    ${B}where${n} before = qsort ${B}\$${n} ${y}filter${n} (<  x) xs
          after  = qsort ${B}\$${n} ${y}filter${n} (>= x) xs

main = ${y}putStrLn${n} ${B}\$${n} ${g}\"Sorted list: \"${n} ++ (${y}show${n} (qsort [${r}7${n},-${r}2${n},${r}4${n},-${r}8${n},${r}6${n},${r}1${n}]))
"


src_java="
import java.util.*;

public class QuickSortTest {

    public static void quickSort(Object[] array) {
        Object pivot, tmp;
        int lw, rw;
        for (;;) {
            while (array[lw] < pivot) lw++;
            while (pivot < array[rw]) rw--;
            if (lw < rw) {
                tmp = array[lw];
                array[lw] = array[rw];
                array[rw] = tmp;
            }
        }
    }

    public static void main(String args[]) {
        int arr1[] = new int[10];
        for (int i=1; i<10; i++) {
            arr1[i] = (int)(Math.random() * 100);
        }

        int arr2[];
        arr2 = (int[])arr1.clone();

        Arrays.sort(arr1);  // sorted by Arrays' method
        quickSort(arr2);  // sorted by self implemented method.

        if (Arrays.equals(arr1, arr2))
            System.out.println(\"The arr1 and the arr2 have a same sequence.\");
        else
            System.out.println(\"The arr1 and the arr2 have different sequences each other.\");
    }
}
"

while [ "$1" != "" ]; do
    if [ "$1" = 'c' ];then
        echo -e "$src_c"
    elif [ "$1" = 'py' ];then
        echo -e "$src_py"
    elif [ "$1" = 'hs' ];then
        echo -e "$src_hs"
    fi
    shift 1
done

