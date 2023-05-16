# rm -rf dist && mkdir dist

cd extractor

VER=`cat extractor.py | grep "__version__ = " | awk -F "\"" '{print $2}'`
# VARIANT=cdrx
VARIANT=batonogov

printf "\n\n>> Building extractor for windows\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-windows"
mv dist/windows/extractor.exe ../dist/extractor-$VER.exe

printf "\n\n>> Building extractor for linux\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-linux"
mv dist/linux/extractor ../dist/extractor-$VER

rm -rf dist
cd ..

cd integrator

VER=`cat integrator.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

printf "\n\n>> Building integrator for windows\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-windows" "pyinstaller --clean -y --dist ./dist/windows --workpath /tmp integrator.spec && chown -R --reference=. ./dist/windows"
mv dist/windows/integrator.exe ../dist/integrator-$VER.exe

printf "\n\n>> Building integrator for linux\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-linux"  "pyinstaller --clean -y --dist ./dist/linux --workpath /tmp integrator.spec && chown -R --reference=. ./dist/linux"
mv dist/linux/integrator ../dist/integrator-$VER

rm -rf dist
# cd ../integrator

VER=`cat indexgenerator.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

printf "\n\n>> Building indexgenerator for windows\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-windows" "pyinstaller --clean -y --dist ./dist/windows --workpath /tmp indexgenerator.spec && chown -R --reference=. ./dist/windows"
mv dist/windows/indexgenerator.exe ../dist/indexgenerator-$VER.exe

printf "\n\n>> Building indexgenerator for linux\n\n"
docker run -v "$(pwd):/src/" "$VARIANT/pyinstaller-linux"  "pyinstaller --clean -y --dist ./dist/linux --workpath /tmp indexgenerator.spec && chown -R --reference=. ./dist/linux"
mv dist/linux/indexgenerator ../dist/indexgenerator-$VER

rm -rf dist
cd ..

# remove containers with the given image name
docker ps -a | awk '{ print $1,$2 }' | grep "$VARIANT/pyinstaller" | awk '{print $1}' | xargs -I {} docker rm -f {}
