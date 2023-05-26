import { TailwindProvider } from 'tailwind-rn';
import utilities from './tailwind.json';
import { NavigationContainer } from '@react-navigation/native';
import RootNavtor from './Navtor/RootNavtor';
import { StyleSheet } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

export default function App() {
  return (
    // @ts-ignore - awdadw
    <TailwindProvider utilities={utilities}>
      <NavigationContainer>
        <RootNavtor />


      </NavigationContainer>

    </TailwindProvider>
  );
};



const styles = StyleSheet.create({
  container: {

  },
});


