import React, { useState } from "react";
import { View, Text, TextInput, Button, Alert, ScrollView } from "react-native";
import axios from "axios";

export default function App() {
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    mechanical_ventilation: "",
    iontropes: "",
    neurological_sequelae: "",
    admission_source: "",
    cpr_24hrs: "",
    cancer: "",
    high_risk_system: "",
    systolic_blood_pressure: "",
    heart_rate: "",
    temperature: "",
    pupil_response: "",
    gcs: "",
    ph: "",
    hco3: "",
    pco2: "",
    po2: "",
    grbs: "",
    k: "",
    creatinine: "",
    urea: "",
    tc: "",
    inr: "",
    aptt: ""
  });

  const handleChange = (name, value) => {
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    const formattedData = {
      "Age": Number(formData.age),
      "Gender(0=female,1=male)": formData.gender.toLowerCase() === "male" ? 1 : 0,
      "Mechanical_ventilation": formData.mechanical_ventilation.toLowerCase() === "yes" ? 1 : 0,
      "Iontropes": formData.iontropes.toLowerCase() === "yes" ? 1 : 0,
      "Neurological_sequelae": formData.neurological_sequelae.toLowerCase() === "yes" ? 1 : 0,
      "Admission_source": Number(formData.admission_source),
      "CPR_within_24hrs_before_PICU_admission": formData.cpr_24hrs.toLowerCase() === "yes" ? 1 : 0,
      "Cancer": formData.cancer.toLowerCase() === "yes" ? 1 : 0,
      "High_risk_system": formData.high_risk_system.toLowerCase() === "yes" ? 1 : 0,
      "Systolic_blood_pressure": Number(formData.systolic_blood_pressure),
      "heart_rate": Number(formData.heart_rate),
      "Temperature": Number(formData.temperature),
      "Pupil": Number(formData.pupil_response),
      "Glasgow_coma_scale_GCS": Number(formData.gcs),
      "PH": Number(formData.ph),
      "HCO3": Number(formData.hco3),
      "PCO2": Number(formData.pco2),
      "PO2": Number(formData.po2),
      "GRBS": Number(formData.grbs),
      "K": Number(formData.k),
      "CREATININE": Number(formData.creatinine),
      "UREA": Number(formData.urea),
      "TC": Number(formData.tc),
      "INR": Number(formData.inr),
      "APTT": Number(formData.aptt),
      "PH_outlier": 0,
      "HCO3_outlier": 0,
      "Prism_score_Binary": 0
    };

    console.log("Sending Data:", formattedData);

    try {
      const response = await axios.post("https://icu-prediction-api.onrender.com/predict", formattedData);
      console.log("Response received:", response.data);
      Alert.alert("Prediction Result", JSON.stringify(response.data));
    } catch (error) {
      console.error("Fetch Error:", error.response?.data || error.message);
      Alert.alert("Error", "Failed to fetch prediction");
    }
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 10 }}>Enter Patient Data</Text>

      {Object.keys(formData).map((key) => (
        <View key={key} style={{ marginBottom: 10 }}>
          <Text>{key.replace(/_/g, " ").toUpperCase()}:</Text>
          <TextInput
            style={{
              borderWidth: 1,
              borderColor: "#ccc",
              padding: 8,
              borderRadius: 5,
              marginTop: 5
            }}
            value={formData[key]}
            onChangeText={(value) => handleChange(key, value)}
            keyboardType="numeric"
          />
        </View>
      ))}

      <Button title="Get Prediction" onPress={handleSubmit} />
    </ScrollView>
  );
}
