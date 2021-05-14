rm -rf dist/*

cd extractor

printf "\n\n>> Building extractor for windows\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
mv dist/windows/extractor.exe ../dist

printf "\n\n>> Building extractor for linux\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
mv dist/linux/extractor ../dist

rm -rf dist
cd ../integrator

printf "\n\n>> Building integrator for windows\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
mv dist/windows/integrator.exe ../dist

printf "\n\n>> Building integrator for linux\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
mv dist/linux/integrator ../dist

rm -rf dist
cd ..