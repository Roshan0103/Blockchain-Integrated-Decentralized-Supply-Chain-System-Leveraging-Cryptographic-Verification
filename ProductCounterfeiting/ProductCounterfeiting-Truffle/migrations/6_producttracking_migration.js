const ProductTracking = artifacts.require("ProductTrackingContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(ProductTracking);
        };
        