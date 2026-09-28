import { StatusBar } from 'expo-status-bar';
import { View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { useFonts, Oswald_700Bold } from '@expo-google-fonts/oswald';
import { Manrope_500Medium, Manrope_700Bold, Manrope_800ExtraBold } from '@expo-google-fonts/manrope';
import { HomeScreen } from './src/screens/HomeScreen';

export default function App() {
  const [fontsLoaded] = useFonts({ Oswald_700Bold, Manrope_500Medium, Manrope_700Bold, Manrope_800ExtraBold });

  if (!fontsLoaded) return <View style={{ flex: 1, backgroundColor: '#FF292B' }} />;

  return (
    <SafeAreaProvider>
      <StatusBar style="dark" />
      <HomeScreen />
    </SafeAreaProvider>
  );
}
