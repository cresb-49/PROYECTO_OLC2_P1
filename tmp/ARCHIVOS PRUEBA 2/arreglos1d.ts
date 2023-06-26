function swap(i: number, j: number, arr: any[]) {
    let temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

function bubbleSort(arr: any[]) {
    for (let i = 0; i < length(arr) - 1; i++) {
        for (let j = 1; j < length(arr) - 1; j++) {
        if (arr[j] > arr[j + 1]) {
            swap(j, j + 1, arr);
        }
        }
    }
}

function insertionSort(arr: any[]) {
    for (let i = 1; i < length(arr); i++) {
        let j = i;
        let temp = arr[i];
        while (j > 0 && arr[j - 1] > temp) {
        arr[j] = arr[j - 1];
        j = j - 1;
    }
    arr[j] = temp;
    }
}

let arreglo = [32, 7 * 3, 7, 89, 56, 909, 109, 2, 9, 9874 * 0, 44, 3, 820 * 10, 11, 8 * 0 + 8, 10];
bubbleSort(arreglo);
for (const iterator of arreglo) {
    console.log("BubbleSort => ", iterator);
}