from flask import Flask, request, jsonify
from similar_neeri import find_similar_expertise ,nlp,model,expertise_data#[, expertise_data] # Assuming you have this function
import json

app = Flask(__name__)


  

@app.route('/get_similar_skill', methods=['POST'])
def get_similar_skill():
    try:
        # Get skill from the request
        data = request.json
        skill_name = data.get('skill')
        with open('expertise.json', 'r') as json_file:
          expertise_data = json.load(json_file)
        # Call the function from 'loop_way_of_doing.ipynb'
        skill_name =skill_name.title()
        similar_skill = find_similar_expertise(skill_name, expertise_data)
        k = 1
        new_list_akill = []
        if len(similar_skill)==0:
          new = {}
          new["name"] = skill_name
          new['subOptions'] = [skill_name]
          expertise_data["expertise"].append(new)
        else:
          for entry in similar_skill:
            inner_new_list_skill= ""
            if entry["Similarity"] > 0.66:
              inner_new_list_skill+=f"Category: {entry['Category']}, Similar Expertise: {entry['Expertise']}, Similarity: {entry['Similarity']:.4f}"# it been recored in a wrong wale.
              if entry["Similarity"] - k == 0:
                k = k-entry["Similarity"]
            new_list_akill.append(inner_new_list_skill)
          if k!=0:
            other_expertise = next(item for item in expertise_data["expertise"] if item["name"] == similar_skill[0]['Category'])#similar_expertise[0]
            other_expertise["subOptions"].append(skill_name)
          # else:
            #   # other_expertise = next(item for item in expertise_data["expertise"] if item["name"] == "Other")
            #   # other_expertise["subOptions"].append(i)
            # new = {}
            # new["name"] = skill_name
            # new['subOptions'] = [skill_name]
            # expertise_data["expertise"].append(new)
        expertise_data = expertise_data
        with open("expertise.json", "w") as outfile: 
          json.dump(expertise_data, outfile)
        

        # Return the result
        return jsonify({'result': new_list_akill})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
