using UnityEngine;
using System.Collections;
using System;

public class Heap<T> where T : IHeapItem<T>

{

	T[] items;

	void SortUp(T item)

                {
		int parentIndex = (item.HeapIndex - 1) / 2;

		while (true)

                                {
			T parentItem = items [parentIndex];
			if (item.CompareTo(parentItem) > 0)

                                                {
				Swap (item, parentItem);
			}

                                                else
                                                {

                                                {
				break;
			}

			parentIndex = (item.HeapIndex - 1) / 2;
		}
	}
}
