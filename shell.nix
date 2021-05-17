{ sources ? import ./nix/sources.nix }:

with import sources.nixpkgs {};

mkShell {
  name = "vaobtsd-env";
  buildInputs = [
    python38
    python38Packages.wheel
    python38Packages.poetry
    python38Packages.numpy
    python38Packages.cython
    clang_10
    llvm
    llvmPackages.openmp
    gcc
    nodejs-12_x
    glibcLocales
  ];
  shellHook = ''
  # set SOURCE_DATE_EPOCH so that we can use python wheels
  export SOURCE_DATE_EPOCH=315532800
  export LD_LIBRARY_PATH=${stdenv.lib.makeLibraryPath [stdenv.cc.cc]}
  '';
  preferLocalBuild = true;
}
