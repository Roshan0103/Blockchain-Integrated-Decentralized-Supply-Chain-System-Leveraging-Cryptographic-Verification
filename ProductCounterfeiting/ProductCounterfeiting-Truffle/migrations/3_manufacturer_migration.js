const Manufacturer = artifacts.require("ManufacturerContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Manufacturer);
        };
        