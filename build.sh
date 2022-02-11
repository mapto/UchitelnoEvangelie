rm -rf dist && mkdir dist

cd extractor

printf "\n\n>> Building extractor for windows\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
mv dist/windows/extractor.exe ../dist

printf "\n\n>> Building extractor for linux\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
mv dist/linux/extractor ../dist

rm -rf dist
cd ../integrator

cd integrator

printf "\n\n>> Building integrator for windows\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --clean -y --dist ./dist/windows --workpath /tmp integrator.spec && chown -R --reference=. ./dist/windows"
mv dist/windows/integrator.exe ../dist

printf "\n\n>> Building integrator for linux\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux  "pyinstaller --clean -y --dist ./dist/linux --workpath /tmp integrator.spec && chown -R --reference=. ./dist/linux"
mv dist/linux/integrator ../dist

rm -rf dist
# cd ../integrator

printf "\n\n>> Building indexgenerator for windows\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --clean -y --dist ./dist/windows --workpath /tmp indexgenerator.spec && chown -R --reference=. ./dist/windows"
mv dist/windows/indexgenerator.exe ../dist

printf "\n\n>> Building indexgenerator for linux\n\n"
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux  "pyinstaller --clean -y --dist ./dist/linux --workpath /tmp indexgenerator.spec && chown -R --reference=. ./dist/linux"
mv dist/linux/indexgenerator ../dist

rm -rf dist
cd ..

# remove containers with the given image name
docker ps -a | awk '{ print $1,$2 }' | grep 'cdrx/pyinstaller' | awk '{print $1}' | xargs -I {} docker rm -f {}
