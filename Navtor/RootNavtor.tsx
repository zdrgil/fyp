import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import TabNavtor from './TabNavtor';
import RegisterScreen from '../screen/RegisterScreen';

export type RootstackParamList = {
    Main: undefined;
    Register: undefined;

}

const Rootstack = createNativeStackNavigator();
const RootNavtor = () => {

    return (
        <Rootstack.Navigator>
            <Rootstack.Group>
                <Rootstack.Screen name="Main" component={TabNavtor} />

            </Rootstack.Group>
            <Rootstack.Group>
                <Rootstack.Screen name="Register" component={RegisterScreen}
                    options={{ headerTransparent: true }} />


            </Rootstack.Group>


        </Rootstack.Navigator>
    )
}

export default RootNavtor




