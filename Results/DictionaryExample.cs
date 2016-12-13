using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class DictionaryExample : MonoBehaviour
{

	private Dictionary<string, int> potionRestoreAmounts;


	// Use this for initialization
	void Start ()
    {
		potionRestoreAmounts =
			new Dictionary<string, int>()
            {
			{"Small", 100},
			{"Medium", 200},
			{"Big", 400},
		};
	}
	
	// Update is called once per frame
	void Update ()
    {
	
	}
}
