const ProductionReceipts = artifacts.require("ProductionReceiptsContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(ProductionReceipts);
        };
        