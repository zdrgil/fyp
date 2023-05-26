import { View, Text, SafeAreaView, ScrollView, ActivityIndicator, RefreshControl, StyleSheet } from 'react-native';
import React, { useEffect, useLayoutEffect, useState } from 'react';
import { useTailwind } from 'tailwind-rn/dist';
import { CompositeNavigationProp, useIsFocused, useNavigation } from '@react-navigation/native';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { TabStackParamList } from '../Navtor/TabNavtor';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootstackParamList } from '../Navtor/RootNavtor';
import { Image } from '@rneui/themed';
import axios from 'axios';
import Refresh from '../component/Refresh';
import Loading from '../component/Loading';



export type CustomerScreenNavigationProp = CompositeNavigationProp<
  BottomTabNavigationProp<TabStackParamList, 'Customer'>,
  NativeStackNavigationProp<RootstackParamList>
>


interface IDoctor {
  id: number;
  name: string;
  state: string;
  clinic: number;
}

interface IClinic {
  id: number;
  clinicname: string;
  location: string;
  telnum: string;
  state: string;
  doctors: IDoctor[]; // Update the type to an array of IDoctor objects
}

const Customerscreen = () => {
  const tw = useTailwind();
  const navigation = useNavigation<CustomerScreenNavigationProp>();
  const [loading, setLoading] = useState<boolean>(false);
  const [clinicdata, setClinicData] = useState<IClinic[]>([]);
  const isFocused = useIsFocused();




  const fetchClinic = async () => {
    try {
      const response = await axios.get<IClinic[]>('http://192.168.110.91:8000/api/clinics/');
      setClinicData(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchClinic();



  }, [isFocused]);

  useLayoutEffect(() => {
    navigation.setOptions({
      headerShown: false,
    })
  }, [])

  if (loading) {
    setTimeout(() => {
      setLoading(false);
    }, 700); // 0.5秒的延迟时间
    return <Loading />;
  }

  return (
    <Refresh onRefresh={fetchClinic}>
      <ScrollView>
        {clinicdata.map((clinic) => (
          <View style={styles.container} key={clinic.id}>
            <View style={styles.pricingOption}>
              <Text style={styles.pricingOptionTitle}> {clinic.clinicname}</Text>
              <Text style={styles.pricingOptionPrice}>{clinic.location}</Text>
              <Text style={styles.pricingOptionDescription}>Tel. {clinic.telnum}</Text>
              <Text style={styles.pricingOptionFeature}>State: {clinic.state}</Text>
              {clinic.doctors.map((doctor) => (
                <View key={doctor.id}>
                  <Text style={styles.pricingOptionPrice}>Doctor:{doctor.name},{doctor.state}</Text>

                </View>
              ))}
              <View style={styles.pricingOptionButtonContainer}>
                <Text style={styles.pricingOptionPrice}></Text>

              </View>
            </View>
          </View>
        ))}
      </ScrollView>
    </Refresh>
  );
}

export default Customerscreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 50,

  },
  pricingOption: {
    margin: 10,
    padding: 20,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    backgroundColor: "#bee9f7",
    width: 380,


  },
  pricingOptionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,


  },
  pricingOptionPrice: {
    fontSize: 18,
    color: '#333',
    marginBottom: 10,
  },
  pricingOptionDescription: {
    fontSize: 14,
    color: '#333',
    marginBottom: 10,
  },
  pricingOptionFeatures: {
    marginBottom: 10,

  },
  pricingOptionFeature: {
    fontSize: 14,
    color: '#333',

  },
  pricingOptionButtonContainer: {
    backgroundColor: '#00BFFF',
    borderRadius: 5,
  },
  pricingOptionButton: {
    fontSize: 14,
    color: '#fff',
    padding: 10,
  },

})
