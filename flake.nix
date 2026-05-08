# ~/workspace/intro-path-planning/flake.nix
{
  description = "Python jupyter env for IKPI path planning";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    # get system specific os info
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
	  packages = [
	    (pkgs.python312.withPackages (ps: with ps; [
	      numpy
	      jupyter
	      scypi
	      pandas
	      matplotlib
	      shapely
	      networkx
	    ]))
	  ];
        };
      }
    );
}
