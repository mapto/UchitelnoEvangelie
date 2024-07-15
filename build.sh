# rm -rf dist && mkdir dist

# IMAGE=cdrx
# IMAGE=batonogov
IMAGE=mruskov
TAG=master
PLATFORMS="windows linux osx"
APPS="extractor integrator indexgenerator atergogenerator"

for APP in $APPS; do
    if [ "$APP" = "extractor" ]; then
        DIR="extractor"
    else
        DIR="integrator"
    fi

    cd $DIR
    VER=`cat $APP.py | grep "__version__ = " | awk -F "\"" '{print $2}'`

    for VAR in $PLATFORMS; do
        if [ "$VAR" = "windows" ]; then
            EXT=".exe"
        else
            EXT=""
        fi
        printf "\n\n>> Building $APP for $VAR\n\n"
        docker run -v "$(pwd):/src/" "$IMAGE/pyinstaller-$VAR:$TAG"
        mv dist/$APP$EXT ../dist/$APP-$VER-$VAR$EXT
    done

    rm -rf dist
    cd ..
done

# remove containers with the given image name
docker ps -a | awk '{ print $1,$2 }' | grep "$IMAGE/pyinstaller" | awk '{print $1}' | xargs -I {} docker rm -f {}
