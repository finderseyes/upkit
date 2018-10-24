using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(UnityEngine.UI.Text))]
public class DemoBehaviour : MonoBehaviour {

    public string helloName = "there";

	// Use this for initialization
	void Start () {
        var text = GetComponent<UnityEngine.UI.Text>();
        text.text = string.Format("Hello {0}, this is demo-package.", helloName);
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
