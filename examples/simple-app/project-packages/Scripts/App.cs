using Newtonsoft.Json;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class App : MonoBehaviour {

    void OnGUI()
    {
        var data = new Item[]
        {
            new Item { Name = "Sword", Value = 100 },
            new Item { Name = "Club", Value = 200 },
        };

        var serializedData = JsonConvert.SerializeObject(data, Formatting.None);
        
        GUI.Box(new Rect(10, 10, 500, 30), "This is a demonstration that the project has been created successfully.");
        GUI.Box(new Rect(10, 50, 500, 60), string.Format("Serialized data: \n {0}", serializedData));

    }
}
