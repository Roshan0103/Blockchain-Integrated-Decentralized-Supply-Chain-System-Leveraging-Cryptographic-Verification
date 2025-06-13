const Vehicle = artifacts.require("VehicleContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Vehicle);
        };
        