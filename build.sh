# rm -rf dist && mkdir dist

# IMAGE=cdrx
# IMAGE=batonogov
IMAGE=mruskov
TAG=master
PLATFORMS="windows linux osx"

cd extractor

VER=`cat extractor.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

for VAR in $PLATFORMS; do
    if [ "$VAR" = "windows" ]; then
        EXT=".exe"
    else
        EXT=""
    fi
    printf "\n\n>> Building extractor for $VAR\n\n"
    docker run -v "$(pwd):/src/" "$IMAGE/pyinstaller-$VAR:$TAG"
    mv dist/extractor$EXT ../dist/extractor-$VER-$VAR$EXT
done

rm -rf dist
cd ..

cd integrator

VER=`cat integrator.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

for VAR in $PLATFORMS; do
    if [ "$VAR" = "windows" ]; then
        EXT=".exe"
    else
        EXT=""
    fi
    printf "\n\n>> Building integrator for $VAR\n\n"
    docker run -v "$(pwd):/src/" "$IMAGE/pyinstaller-$VAR:$TAG" "pyinstaller --clean -y --dist ./dist/$VAR --workpath /tmp integrator.spec && chown -R --reference=. ./dist/$VAR"
    mv dist/$VAR/integrator$EXT ../dist/integrator-$VER-$VAR$EXT
done

rm -rf dist
# cd ../integrator

VER=`cat indexgenerator.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

for VAR in $PLATFORMS; do
    if [ "$VAR" = "windows" ]; then
        EXT=".exe"
    else
        EXT=""
    fi
    printf "\n\n>> Building indexgenerator for $VAR\n\n"
    docker run -v "$(pwd):/src/" "$IMAGE/pyinstaller-$VAR:$TAG" "pyinstaller --clean -y --dist ./dist/$VAR --workpath /tmp indexgenerator.spec && chown -R --reference=. ./dist/$VAR"
    mv dist/$VAR/indexgenerator$EXT ../dist/indexgenerator-$VER-$VAR$EXT
done

rm -rf dist
cd ..

# remove containers with the given image name
docker ps -a | awk '{ print $1,$2 }' | grep "$IMAGE/pyinstaller" | awk '{print $1}' | xargs -I {} docker rm -f {}
